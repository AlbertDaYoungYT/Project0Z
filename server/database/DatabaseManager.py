
import redis
import loguru
import asyncio
import couchdb

from config.ConfigContainer import ConfigContainer
from database.models import DataStores, Model
from connectors.DatabaseLink import DatabaseLinkConnector
from task.TaskSystem import TaskScheduler
from utils.DatabaseAdapter import Serializable


class RedisDBManager:

    def __init__(self, config: ConfigContainer, db: DataStores = DataStores.DEFAULT):
        self.config = config
        self.server = None
        self.server_db = db

        self.is_cache_instance_link: bool = False
        self.instance_link: DatabaseLinkConnector = None

        self._connect()

    def _connect(self):
        """Connect to the RedisDB server."""
        try:
            self.server = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                password=self.config.redis_pass,
                db=self.server_db.value
            )
            loguru.logger.info(f"Connected to Redis-{self.server_db.name} server at {self.config.redis_host}:{self.config.redis_port}")
        except Exception as e:
            loguru.logger.error(f"Failed to connect to Redis server: {e}")
            self.server = None
    
    def _disconnect(self):
        try:
            self.server.close()
        except Exception as e:
            loguru.logger.error(f"Error trying to close Redis Server Connection: {e}")
            return False
        return True

    def _link_as_cache(self, other: DatabaseLinkConnector) -> bool:
        try:
            self.is_cache_instance_link = True
            self.instance_link = other
        except Exception as e:
            loguru.logger.error(f"Error trying to link Redis Server Connection: {e}")
            return False

        if self.server == None:
            loguru.logger.error(f"Error trying to link Redis Server Connection")
            return False
        return True

    async def add(self, key: str, value: Model, **kwargs):
        """Add an item to the Redis database."""
        if self.server is None:
            loguru.logger.error("Redis server not connected.")
            return False
        try:
            if self.is_cache_instance_link:
                res = await asyncio.to_thread(self.server.set, key, value.to_json(), ex=self.config.cache_expire_time_seconds, **kwargs)
            else:
                res = await asyncio.to_thread(self.server.set, key, value.to_json(), **kwargs)
            if res is True:
                loguru.logger.debug(f"Item added to 'DataStore-{self.server_db}' with key: {key}")
                return True
            else:
                loguru.logger.error(f"Failed to add item to 'DataStore-{self.server_db}': {res}")
                return False
        except Exception as e:
            loguru.logger.error(f"Error adding item to 'DataStore-{self.server_db}': {e}")
            return False

    async def get(self, key: str, clazz: Model):
        """Retrieve an item from the Redis database by its key."""
        if self.server is None:
            loguru.logger.error("Redis server not connected.")
            return None
        try:
            value = await asyncio.to_thread(self.server.get, key)
            if value is not None:
                loguru.logger.debug(f"Item retrieved from 'DataStore-{self.server_db}' with key: {key}")
                return clazz.from_json(value)
            else:
                loguru.logger.warning(f"No item found with key '{key}' in 'DataStore-{self.server_db}'.")
                return None
        except Exception as e:
            loguru.logger.error(f"Error retrieving item from 'DataStore-{self.server_db}': {e}")
            return None

    async def delete(self, key: str):
        """Delete an item from the Redis database by its key."""
        if self.server is None:
            loguru.logger.error("Redis server not connected.")
            return False
        try:
            res = await asyncio.to_thread(self.server.delete, key)
            if res == 1:
                loguru.logger.debug(f"Item deleted from 'DataStore-{self.server_db}' with key: {key}")
                return True
            elif res == 0:
                loguru.logger.warning(f"No item found with key '{key}' in 'DataStore-{self.server_db}'.")
                return False
            else:
                loguru.logger.error(f"Failed to delete item from 'DataStore-{self.server_db}': {res}")
                return False
        except Exception as e:
            loguru.logger.error(f"Error deleting item from 'DataStore-{self.server_db}': {e}")
            return False

    async def exists(self, key: str):
        """Check if an item exists in the Redis database by its key."""
        if self.server is None:
            loguru.logger.error("Redis server not connected.")
            return False
        try:
            res = await asyncio.to_thread(self.server.exists, key)
            if res == 1:
                loguru.logger.debug(f"Item exists in 'DataStore-{self.server_db}' with key: {key}")
                return True
            else:
                loguru.logger.info(f"No item found with key '{key}' in 'DataStore-{self.server_db}'.")
                return False
        except Exception as e:
            loguru.logger.error(f"Error checking existence of item in 'DataStore-{self.server_db}': {e}")
            return False
        

class CouchDBManager:

    def __init__(self, task_scheduler: TaskScheduler, server_url: str, config: ConfigContainer, cache_server: DatabaseLinkConnector | None = None):
        self.server_url = server_url
        self.config = config
        self.server = None

        self.task_scheduler = task_scheduler

        self.cache_instance_link: DatabaseLinkConnector | None = cache_server
        self._connect()

    def _connect(self):
        """Connect to the CouchDB server."""
        try:
            self.server = couchdb.Server(self.server_url)
            self.server.resource.credentials = (self.config.couchdb_user, self.config.couchdb_pass)
            self.server.login(self.config.couchdb_user, self.config.couchdb_pass)
            loguru.logger.info(f"Connected to CouchDB server at {self.server_url}")
        except Exception as e:
            loguru.logger.error(f"Failed to connect to CouchDB server: {e}")
            self.server = None

    def _link_to_cache(self, db: DataStores = DataStores.DEFAULT):
        loguru.logger.info(f"Attempting to Link CouchDB to Redis Cache Instance...")
        self.cache_instance_link = DatabaseLinkConnector(
            RedisDBManager(self.config, db=db),
            self
        )
        self.cache_instance_link.redis._link_as_cache(self.cache_instance_link)

    def get_database(self, db_name: str):
        """Get a specific database. Creates it if it doesn't exist."""
        if self.server is None:
            loguru.logger.error("CouchDB server not connected.")
            return None
        try:
            db = self.server[db_name]
            return db
        except couchdb.ResourceNotFound:
            loguru.logger.info(f"Database '{db_name}' not found. Creating it.")
            try:
                db = self.server.create(db_name)
                return db
            except Exception as e:
                loguru.logger.error(f"Failed to create database '{db_name}': {e}")
                return None
        except Exception as e:
            loguru.logger.error(f"Error accessing database '{db_name}': {e}")
            return None

    async def save_document(self, db_name: str, document: Serializable):
        """Save a document to the specified database."""
        db = self.get_database(db_name)
        if db:
            try:
                doc_id, doc_rev = await asyncio.to_thread(db.save, document.to_dict())
                if self.cache_instance_link != None:
                    await self.task_scheduler.submit(self.cache_instance_link.redis.add, doc_id, document.to_json())
                loguru.logger.debug(f"Document saved to '{db_name}' with ID: {doc_id}, Revision: {doc_rev}")
                return doc_id, doc_rev
            except Exception as e:
                loguru.logger.error(f"Failed to save document to '{db_name}': {e}")
                return None
        return None

    async def get_document(self, db_name: str, doc_id: str) -> Serializable:
        """Retrieve a document from the specified database by its ID."""
        db = self.get_database(db_name)
        if db:
            try:
                if self.cache_instance_link != None:
                    res = await self.cache_instance_link.redis.get(doc_id, document.to_json())
                    if res == None:
                        document = await asyncio.to_thread(db.get, doc_id)
                    else:
                        document = Serializable.from_json(res)
                else:
                    document = Serializable.from_dict(await asyncio.to_thread(db.get, doc_id))
                return document
            except couchdb.ResourceNotFound:
                loguru.logger.warning(f"Document with ID '{doc_id}' not found in '{db_name}'.")
                return None
            except Exception as e:
                loguru.logger.error(f"Failed to retrieve document '{doc_id}' from '{db_name}': {e}")
                return None
        return None

    async def delete_document(self, db_name: str, doc_id: str):
        """Delete a document from the specified database by its ID and revision."""
        db = self.get_database(db_name)
        if db:
            try:
                await asyncio.to_thread(db.delete, doc_id)
                loguru.logger.debug(f"Document '{doc_id}' deleted from '{db_name}'.")
                return True
            except couchdb.ResourceNotFound:
                loguru.logger.warning(f"Document with ID '{doc_id}' not found in '{db_name}'.")
                return False
            except couchdb.ResourceConflict:
                loguru.logger.error(f"Conflict deleting document '{doc_id}' in '{db_name}'. Revision mismatch.")
                return False
            except Exception as e:
                loguru.logger.error(f"Failed to delete document '{doc_id}' from '{db_name}': {e}")
                return False
        return False

    async def find_documents(self, db_name: str, query: dict) -> list[Serializable]:
        """Find documents in the specified database based on a query."""
        db = self.get_database(db_name)
        if db:
            try:
                result = await asyncio.to_thread(db.find, query)
                return [Serializable.from_dict(x) for x in list(result)]
            except Exception as e:
                loguru.logger.error(f"Error executing find query on '{db_name}': {e}")
                return []
        return []
    
    # TODO: Add more generic database interaction methods as needed (e.g., list all docs, etc.)

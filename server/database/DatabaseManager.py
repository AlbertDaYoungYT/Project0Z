
import redis
import loguru
import asyncio
import couchdb

from config.ConfigContainer import ConfigContainer


class CouchDBManager:

    def __init__(self, server_url: str, config: ConfigContainer):
        self.server_url = server_url
        self.config = config
        self.server = None
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

    async def save_document(self, db_name: str, document: dict):
        """Save a document to the specified database."""
        db = self.get_database(db_name)
        if db:
            try:
                doc_id, doc_rev = await asyncio.to_thread(db.save, document)
                loguru.logger.debug(f"Document saved to '{db_name}' with ID: {doc_id}, Revision: {doc_rev}")
                return doc_id, doc_rev
            except Exception as e:
                loguru.logger.error(f"Failed to save document to '{db_name}': {e}")
                return None
        return None

    async def get_document(self, db_name: str, doc_id: str):
        """Retrieve a document from the specified database by its ID."""
        db = self.get_database(db_name)
        if db:
            try:
                document = await asyncio.to_thread(db.get, doc_id)
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

    async def find_documents(self, db_name: str, query: dict):
        """Find documents in the specified database based on a query."""
        db = self.get_database(db_name)
        if db:
            try:
                result = await asyncio.to_thread(db.find, query)
                return list(result)
            except Exception as e:
                loguru.logger.error(f"Error executing find query on '{db_name}': {e}")
                return []
        return []
    
    # Add more generic database interaction methods as needed (e.g., list all docs, etc.)



class RedisDBManager:

    def __init__(self, config: ConfigContainer):
        self.config = config
        self.server = None
        self._connect()

    def _connect(self):
        """Connect to the RedisDB server."""
        try:
            self.server = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                password=self.config.redis_pass,
                db=1
            )
            loguru.logger.info(f"Connected to Redis server at {self.config.redis_host}:{self.config.redis_port}")
        except Exception as e:
            loguru.logger.error(f"Failed to connect to Redis server: {e}")
            self.server = None
        
    def get_redis(self):
        return self.server
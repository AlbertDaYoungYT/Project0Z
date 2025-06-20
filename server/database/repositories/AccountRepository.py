
import loguru

from config.ConfigContainer import ConfigContainer
from database.DatabaseManager import CouchDBManager
from database.Models import *
from server.player.Account import Account


class AccountRepository(CouchDBManager):

    def __init__(self, server: CouchDBManager, server_url: str, config: ConfigContainer):
        self.DATABASE_NAME = config.couchdb_collection + "_accounts"
        self.server_url = server_url
        self.config = config
        self.server = server

        self._link_to_cache(db=DataStores.ACCOUNT)
        loguru.logger.debug(f"Initiated CouchDB Repo: {self.DATABASE_NAME}")

    async def create_account(self, account: Account):
        """Create a new account."""
        doc = account.to_dict()
        result = await self.server.save_document(self.DATABASE_NAME, doc)
        if result:
            account.account_id = result[0]  # Update account ID with the CouchDB ID
            return account
        return None

    async def get_account_by_id(self, account_id: str):
        """Get an account by its ID."""
        doc = await self.server.get_document(self.DATABASE_NAME, account_id)
        if doc:
            return Account.from_dict(doc)
        return None

    async def get_account_by_username(self, username: str):
        """Get an account by its username."""
        query = {"selector": {"username": username}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return Account.from_dict(results[0])
        return None

    async def get_account_by_email(self, email: str):
        """Get an account by its email."""
        query = {"selector": {"email": email}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return Account.from_dict(results[0])
        return None

    async def get_account_by_token(self, token: str):
        """Get an account by its token."""
        query = {"selector": {"token": token}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return Account.from_dict(results[0])
        return None

    async def get_account_by_permission(self, permission: str):
        """Get an account by its permission."""
        query = {"selector": {"permission": permission}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return Account.from_dict(results[0])
        return None

    async def get_account_by_group(self, group: str):
        """Get an account by its group."""
        query = {"selector": {"group": group}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return Account.from_dict(results[0])
        return None

    async def update_account(self, account: Account):
        """Update an existing account."""
        doc = account.to_dict()
        existing_doc = await self.server.get_document(self.DATABASE_NAME, account.account_id)
        if existing_doc:
            doc["_rev"] = existing_doc["_rev"]  # Include the revision for updating
            result = await self.server.save_document(self.DATABASE_NAME, doc)
            return result is not None
        return False

    async def delete_account(self, account_id: str):
        """Delete an account by its ID."""
        return await self.server.delete_document(self.DATABASE_NAME, account_id)

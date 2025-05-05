
import loguru

from config.ConfigContainer import ConfigContainer
from database.DatabaseManager import CouchDBManager
from database.models.PlayerModel import PlayerModel
from database.models import DataStores
from server.player.Player import Player


class PlayerRepository(CouchDBManager):

    def __init__(self, server: CouchDBManager, server_url: str, config: ConfigContainer):
        self.DATABASE_NAME = config.couchdb_collection + "_players"
        self.server_url = server_url
        self.config = config
        self.server = server

        self._link_to_cache(DataStores.PLAYER)
        loguru.logger.debug(f"Initiated CouchDB Repo: {self.DATABASE_NAME}")

    async def create_player(self, player: Player):
        """Create a new player."""
        doc = PlayerModel.from_class(player)
        result = await self.server.save_document(self.DATABASE_NAME, doc.to_dict())
        if result:
            player.id = result[0]  # Update player ID with the CouchDB ID
            return player
        return None

    async def get_player_by_id(self, player_id: str):
        """Get an player by its ID."""
        doc = await self.server.get_document(self.DATABASE_NAME, player_id)
        if doc:
            model = PlayerModel(**doc.items())
            return model.to_class(Player)
        return None

    async def get_player_by_username(self, username: str):
        """Get an player by its username."""
        query = {"selector": {"username": username}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            model = PlayerModel(**results[0].items())
            return model.to_class(Player)
        return None

    async def get_player_by_account_id(self, account_id: str):
        """Get an player by its email."""
        query = {"selector": {"account_id": account_id}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            model = PlayerModel(**results[0].items())
            return model.to_class(Player)
        return None

    async def update_player(self, player: Player):
        """Update an existing player."""
        doc = PlayerModel.from_class(player)
        existing_doc = await self.server.get_document(self.DATABASE_NAME, doc.id)
        if existing_doc:
            doc["_rev"] = existing_doc["_rev"]  # Include the revision for updating
            result = await self.server.save_document(self.DATABASE_NAME, doc.to_dict())
            return result is not None
        return False

    async def delete_player(self, player_id: str):
        """Delete an player by its ID."""
        return await self.server.delete_document(self.DATABASE_NAME, player_id)

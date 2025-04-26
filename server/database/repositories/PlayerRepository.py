
import loguru

from config.ConfigContainer import ConfigContainer
from database.DatabaseManager import CouchDBManager
from database.models.PlayerModel import PlayerModel
from server.player.Player import Player


class PlayerRepository(CouchDBManager):

    def __init__(self, server_url: str, config: ConfigContainer):
        self.DATABASE_NAME = config.collection + "_players"
        super().__init__(server_url, config)

    async def create_player(self, player: Player):
        """Create a new player."""
        doc = PlayerModel.from_class(player)
        result = await self.save_document(self.DATABASE_NAME, doc.to_dict())
        if result:
            player.id = result[0]  # Update player ID with the CouchDB ID
            return player
        return None

    async def get_player_by_id(self, player_id: str):
        """Get an player by its ID."""
        doc = await self.get_document(self.DATABASE_NAME, player_id)
        if doc:
            model = PlayerModel(**doc.items())
            return model.to_class(Player)
        return None

    async def get_player_by_username(self, username: str):
        """Get an player by its username."""
        query = {"selector": {"username": username}}
        results = await self.find_documents(self.DATABASE_NAME, query)
        if results:
            model = PlayerModel(**results[0].items())
            return model.to_class(Player)
        return None

    async def get_player_by_account_id(self, account_id: str):
        """Get an player by its email."""
        query = {"selector": {"account_id": account_id}}
        results = await self.find_documents(self.DATABASE_NAME, query)
        if results:
            model = PlayerModel(**results[0].items())
            return model.to_class(Player)
        return None

    async def update_player(self, player: Player):
        """Update an existing player."""
        doc = PlayerModel.from_class(player)
        existing_doc = await self.get_document(self.DATABASE_NAME, doc.id)
        if existing_doc:
            doc["_rev"] = existing_doc["_rev"]  # Include the revision for updating
            result = await self.save_document(self.DATABASE_NAME, doc.to_dict())
            return result is not None
        return False

    async def delete_player(self, player_id: str, rev: str):
        """Delete an player by its ID and revision."""
        return await self.delete_document(self.DATABASE_NAME, player_id, rev)

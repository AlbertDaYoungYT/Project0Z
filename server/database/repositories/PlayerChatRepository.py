
import secrets
from uuid import UUID
import loguru

from config.ConfigContainer import ConfigContainer
from database.DatabaseManager import CouchDBManager
from database.Models import *

class PlayerChatRepository(CouchDBManager):

    def __init__(self, server: CouchDBManager, server_url: str, config: ConfigContainer):
        self.DATABASE_NAME = config.couchdb_collection + "_player_chats"
        self.server_url = server_url
        self.config = config
        self.server = server

        self._link_to_cache(db=DataStores.CHATS)
        loguru.logger.debug(f"Initiated CouchDB Repo: {self.DATABASE_NAME}")
    
    async def send_message(self, chatModel: PlayerChatModel) -> PlayerChatModel:

        result = await self.server.save_document(self.DATABASE_NAME, chatModel.to_dict())
        if result:
            chatModel.message_id = result[0]  # Update player ID with the CouchDB ID
            return chatModel
        return None

    async def get_messages_by_reciever(self, reciever_id: UUID) -> PlayerChatModel:

        query = {"selector": {"reciever_id": reciever_id}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return PlayerChatModel(**results[0].items())
        return None

    async def get_messages_by_sender(self, sender_id: UUID) -> PlayerChatModel:

        query = {"selector": {"sender_id": sender_id}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return PlayerChatModel(**results[0].items())
        return None
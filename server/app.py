import sys

from config.ConfigContainer import ConfigContainer
from database.repositories.AccountRepository import AccountRepository
from utils.AppServices import AppServices
from GameConstants import GameConstants
from utils.File import File
sys.dont_write_bytecode = True

from dataclasses import dataclass
from enum import Enum
from paprika import *

from aiohttp import web
import loguru
import threading
import asyncio
import socket
import time
import os

from database.DatabaseManager import CouchDBManager
from server.AsyncGameServer import AsyncGameServer
from server.http.HttpServer import HttpServer
from server.player.Account import Account


#TODO: Create a log transport system to sync logcat errors to the server (Maybe via http)
#TODO: Create an admin dashboard for managing game mechanics etc.



class ProjectZ0:

    def __init__(self):
        loguru.logger.info("Loading ProjectZ0...")
        self.services = AppServices()
        if not os.path.exists("./config.json"):
            self.services.config.__save__(File("config.json"))
        else:
            self.services.config.__load__(File("config.json"))
    
    async def start(self):
        loguru.logger.info(f"ProjectZ0 Version: {self.services.game_constants.VERSION}")

        if self.services.game_constants.GIT_BRANCH == "main":
            loguru.logger.info(f"Server Starting in production mode...")
        if self.services.game_constants.GIT_BRANCH == "dev":
            loguru.logger.info(f"Server Starting in development mode...")

        # Start the server in the background
        self.services.game_server = AsyncGameServer(os.getenv("PROJECTZ0_HOST"), os.getenv("GAME_PORT", 23899), self.services)
        await self.services.game_server.start()
        
        self.services.http_server = HttpServer(os.getenv("PROJECTZ0_HOST"), os.getenv("HTTP_PORT", 24899), self.services)
        web_runner = await self.services.http_server.start()
        

        try:
            await asyncio.Future()  # Keep both servers running
        finally:
            await web_runner.cleanup()
            await self.services.game_server.stop() 


    async def _test_database(self):
        new_account = Account(account_id="user123", username="tester", email="test@example.com", token="initial_token")
        created_account = await self.account_repo.create_account(new_account)
        if created_account:
            loguru.logger.info(f"Created account: {created_account.to_dict()}")
            retrieved_account = await self.account_repo.get_account_by_id(created_account.id)
            if retrieved_account:
                loguru.logger.info(f"Retrieved account: {retrieved_account.to_dict()}")
                retrieved_account.token = "updated_token"
                updated = await self.account_repo.update_account(retrieved_account)
                if updated:
                    loguru.logger.info(f"Account updated.")
                    account_by_username = await self.account_repo.get_account_by_username("tester")
                    if account_by_username:
                        loguru.logger.info(f"Account by username: {account_by_username.to_dict()}")
                    # await self.account_repo.delete_account(created_account.id, retrieved_account._rev)
        else:
            loguru.logger.error("Failed to create account.")


    class ServerRunMode(Enum):
        HYBRID         = "HYBRID"
        DISPATCH_ONLY  = "DISPATCH_ONLY"
        GAME_ONLY      = "GAME_ONLY"



asyncio.run(ProjectZ0().start())
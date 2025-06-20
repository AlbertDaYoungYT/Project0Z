import importlib
import io
import pkgutil
import sys
from typing import Dict
import unittest

from config.ConfigContainer import ConfigContainer
from database.repositories.AccountRepository import AccountRepository
from command import *
from server.event import EventHandler
from server.event.server.ServerAssetLoadEvent import ServerAssetLoadEvent
from utils.Testing import BaseTest
from task.TaskSystem import TaskScheduler
from utils.AppServices import AppServices
from GameConstants import GameConstants
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

loguru.logger.remove()
loguru.logger.add(sys.stderr, level="DEBUG")

#TODO: Create a log transport system to sync logcat errors to the server (Maybe via http)
#TODO: Create an admin dashboard for managing game mechanics etc.

#TODO: Move static asset presets into their respective classes in a server/game folder
#TODO: Refactor the whole Project into "core", "utils", "assets", "game", "server", etc.

#TODO: Create a docker-compose.yml file for the server.


def get_test_cases_from_suite(suite):
    """Recursively extracts TestCase instances that inherit from BaseTest."""
    test_cases = []
    try:
        for item in suite:
            if isinstance(item, unittest.TestCase) and issubclass(item.__class__, BaseTest) and item.__class__ != BaseTest:
                test_cases.append(item)
            elif isinstance(item, unittest.TestSuite):
                test_cases.extend(get_test_cases_from_suite(item))
    except TypeError:
        if isinstance(suite, unittest.TestCase) and issubclass(suite.__class__, BaseTest) and suite.__class__ != BaseTest:
            test_cases.append(suite)
    return test_cases

class ProjectZ0:

    def __init__(self):
        loguru.logger.info("Loading ProjectZ0...")
        self.future: asyncio.Future
        self.config = ConfigContainer()
        self.task_scheduler = TaskScheduler(self.config)
        self.command_handlers: Dict[int, CommandHandler] = {}

        if not os.path.exists("./config.json"):
            self.config.__save__(open("config.json", "w"))
        else:
            self.config = self.config.__load__(open("config.json", "r"))
        
        self.services = AppServices(self.config, self.task_scheduler)

        from static import assets
        EventHandler.register_listener(
            self,
            event_class=ServerAssetLoadEvent,
            listener=assets.asset_load_listener
        )

        event = ServerAssetLoadEvent()
        if not event.is_cancelled():
            event.call()

        if os.getenv("SERVER_TEST_MODE", "false") == "true":
            loguru.logger.remove()
            loguru.logger.add(sys.stderr, level="DEBUG")

            loguru.logger.debug(f"Server Initiating Test Mode...")
        
            # Initiate Testing Functions
            from utils.Testing import run_tests, TestPriority
            import tests
            run_tests(log_summary=True)

            exit()
        else:
            from utils.Testing import run_tests, TestPriority
            import tests
            run_tests(priorities_to_run=[TestPriority.CORE, TestPriority.DATABASE, TestPriority.GAME, TestPriority.PERMISSION], log_summary=True)

    
    async def initiate(self):
        loguru.logger.info(f"ProjectZ0 Version: {self.services.game_constants.VERSION}")

        if os.getenv("GIT_BRANCH", "main") == "main":
            loguru.logger.info(f"Server Starting in production mode...")
        if os.getenv("GIT_BRANCH", "main") == "dev":
            loguru.logger.info(f"Server Starting in development mode...")

        # Start the server in the background
        self.services.game_server = AsyncGameServer(os.getenv("PROJECTZ0_HOST", "127.0.0.1"), os.getenv("GAME_PORT", 23899), self.services)
        await self.services.game_server.start()
        
        self.services.http_server = HttpServer(os.getenv("PROJECTZ0_HOST", "127.0.0.1"), os.getenv("HTTP_PORT", 24899), self.services)
        web_runner = await self.services.http_server.start()

        self.console_task = asyncio.create_task(
            self.start_console()
        )  # Start console task
        self.register_commands()  # Register commands
        
        try:
            await self.keep_alive()
        finally:
            await web_runner.cleanup()
            await self.services.game_server.stop()
            if self.console_task:  # Cancel the console task
                self.console_task.cancel()
                try:
                    await self.console_task
                except asyncio.CancelledError:
                    pass
            return

    async def keep_alive(self):
        try:
            self.future = await asyncio.Future()
        finally:
            return

    def register_commands(self):
        """Register command handlers."""
        handler_package = "command.commands"  # The name of your package containing handlers

        try:
            module = importlib.import_module(handler_package)

            # Recursively scan submodules if needed
            for _, module_name, is_pkg in pkgutil.walk_packages(module.__path__, prefix=module.__name__ + "."):
                if not is_pkg:
                    try:
                        sub_module = importlib.import_module(module_name)
                        for name, obj in inspect.getmembers(sub_module):
                            if inspect.isclass(obj) and issubclass(obj, CommandHandler) and obj != CommandHandler:
                                self.register_packet_handler(obj)
                    except ImportError as e:
                        loguru.logger.warning(f"Error importing submodule {module_name}: {e}")

        except ImportError as e:
            loguru.logger.error(f"Could not import command handler package '{handler_package}': {e}")

        loguru.logger.debug(f"Registered {len(self.command_handlers)} {CommandHandler.__name__}s")

    def register_command(self, handler: CommandHandler):
        """Registers a command handler."""
        label = handler.get_label()
        self.command_handlers[label.lower()] = handler
        for alias in getattr(handler.__class__, "command_annotation").aliases:
            self.command_handlers[alias.lower()] = handler

    async def start_console(self):
        """Start the interactive console."""
        loop = asyncio.get_event_loop()
        while True:
            try:
                user_input = await loop.run_in_executor(
                    None, sys.stdin.readline
                )  # Use None for default executor
                user_input = user_input.strip()
                if not user_input:
                    continue
                if user_input.lower() == "stop":
                    loguru.logger.info("Stopping server from console...")
                    # Stop the http server and game server.
                    await self.services.http_server.stop()
                    await self.services.game_server.stop() #  Add this if you have a stop method.
                    self.console_task.cancel()
                    break
                elif user_input.lower() == "help":
                    self.display_command_list() # show available commands
                else:
                    await self.handle_console_command(
                        user_input
                    )  # Await the handler.
            except asyncio.CancelledError:
                loguru.logger.info("Console task cancelled.")
                break
            except Exception as e:
                loguru.logger.error(f"Error reading from console: {e}")
                break

    async def handle_console_command(self, command_string: str):
        """Handle commands entered in the console."""
        parts = command_string.split()
        if not parts:
            return

        command_label = parts[0].lower()
        args = parts[1:]

        handler = self.command_handlers.get(command_label)
        if handler:
            await handler.execute(None, None, args)  #  No sender, no target
        else:
            loguru.logger.error(f"Unknown command: {command_label}")

    def display_command_list(self):
        """Displays a list of registered commands."""
        loguru.logger.info("Available Commands:")
        for label, handler in self.command_handlers.items():
            command_annotation = getattr(handler.__class__, "command_annotation", None)
            if command_annotation:
                description = handler.get_description_string(None)  # No sender for console
                loguru.logger.info(f"  {label}: {description}")
            else:
                loguru.logger.info(f"  {label}: (No description)")


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



async def main():
    """Main entry point."""
    z0_instance = ProjectZ0()
    try:
        await z0_instance.initiate()
    except asyncio.CancelledError:
        loguru.logger.info("Main task was cancelled")
        z0_instance.future.cancel()
    except Exception as e:
        loguru.logger.error(f"Exception in main: {e}")
        z0_instance.future.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        loguru.logger.info("KeyboardInterrupt caught, exiting...")
    finally:
        loguru.logger.info("Application finished.")
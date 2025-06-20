
from typing import Callable

import loguru

from server.event import EventHandler
from server.event.server.ServerAssetErrorEvent import ServerAssetErrorEvent
from utils.AppServices import AppServices
from utils.AssetBridge import LuaBridge


# Expose Functions
def error(message: str):
    EventHandler.dispatch_event(ServerAssetErrorEvent(message))

    loguru.logger.error(message)




def expose(lua_bridge: LuaBridge, python_function: Callable, function_name: str):
    lua_bridge.expose_function_to_lua(python_function, function_name)


def default_expose(lua_bridge: LuaBridge):
    lua_bridge.expose_function_to_lua(loguru.logger.info, "print")
    lua_bridge.expose_function_to_lua(error, "error")


    # Expose a Python function to Lua
    lua_bridge.expose_function_to_lua(loguru.logger.info, "log_info")
    lua_bridge.expose_function_to_lua(loguru.logger.debug, "log_debug")
    lua_bridge.expose_function_to_lua(loguru.logger.warning, "log_warning")
    lua_bridge.expose_function_to_lua(loguru.logger.error, "log_error")

    # Expose Python functions for interacting with the Server
    lua_bridge.expose_function_to_lua(AppServices, "app_services")
    lua_bridge.expose_function_to_lua(EventHandler, "event_handler")
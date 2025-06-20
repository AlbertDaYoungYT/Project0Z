import lupa
import loguru
from typing import Any, Callable
import os

class LuaBridge:
    """
    Manages the Lua runtime and provides a bridge for Python-Lua interoperation.
    """
    def __init__(self, unpack_returned_tuples=True, asset_root_path: str | None = None):
        loguru.logger.info("Initializing LuaBridge and LuaRuntime...")
        try:
            self._lua_runtime = lupa.LuaRuntime(unpack_returned_tuples=unpack_returned_tuples)
            self._lua_globals = self._lua_runtime.globals()
            loguru.logger.success("LuaRuntime initialized successfully.")

            if asset_root_path:
                absolute_asset_root = os.path.abspath(asset_root_path)
                # Replace backslashes with forward slashes for Lua's package.path consistency
                lua_friendly_asset_root = absolute_asset_root.replace('\\', '/')

                # Patterns for Lua's require function:
                # 1. Looks for 'module.lua' (e.g., asset_root/core/effect.lua for require("core.effect"))
                # 2. Looks for 'package/init.lua' (e.g., asset_root/core/init.lua for require("core"))
                new_path_patterns = f"{lua_friendly_asset_root}/?.lua;{lua_friendly_asset_root}/?/init.lua"

                current_package_path = self._lua_globals.package.path
                self._lua_globals.package.path = f"{new_path_patterns};{current_package_path}"
                #loguru.logger.info(f"Prepended to Lua package.path: {new_path_patterns}")
                #loguru.logger.debug(f"New Lua package.path: {self._lua_globals.package.path}")
            else:
                loguru.logger.debug(f"Default Lua package.path: {self._lua_globals.package.path}")

        except Exception as e:
            loguru.logger.critical(f"Failed to initialize LuaRuntime: {e}")
            raise

    @property
    def runtime(self) -> lupa.LuaRuntime:
        """Returns the raw LuaRuntime object."""
        return self._lua_runtime

    @property
    def globals(self) -> Any: # lupa.lua_type.LuaTable
        """Returns the Lua global table."""
        return self._lua_globals

    def execute_lua_file(self, file_path: str) -> Any:
        """
        Loads and executes a Lua file.
        Returns the result of the Lua script (e.g., if it returns a table or function).
        """
        loguru.logger.debug(f"Executing Lua file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lua_code = f.read()
            return self._lua_runtime.execute(lua_code)
        except lupa.LuaError as e:
            loguru.logger.error(f"LuaError executing file {file_path}: {e}")
            raise
        except FileNotFoundError:
            loguru.logger.error(f"Lua file not found: {file_path}")
            raise
        except Exception as e:
            loguru.logger.error(f"Unexpected error executing Lua file {file_path}: {e}")
            raise

    def execute_lua_string(self, lua_code: str) -> Any:
        """
        Executes a string of Lua code.
        Returns the result of the Lua script.
        """
        loguru.logger.trace(f"Executing Lua string: {lua_code[:100]}...") # Log only a part for brevity
        try:
            return self._lua_runtime.execute(lua_code)
        except lupa.LuaError as e:
            loguru.logger.error(f"LuaError executing string: {e}")
            raise
        except Exception as e:
            loguru.logger.error(f"Unexpected error executing Lua string: {e}")
            raise

    def expose_function_to_lua(self, python_function: Callable, lua_function_name: str):
        """
        Exposes a Python function to the Lua global namespace.
        """
        loguru.logger.debug(f"Exposing Python function '{python_function.__name__}' as '{lua_function_name}' to Lua.")
        self._lua_globals[lua_function_name] = python_function

    def get_lua_global(self, name: str) -> Any:
        """
        Retrieves a global variable from the Lua environment.
        """
        loguru.logger.trace(f"Getting Lua global: {name}")
        try:
            return self._lua_globals[name]
        except Exception as e: # Lupa might raise generic exception if key not found
            loguru.logger.warning(f"Could not get Lua global '{name}': {e}")
            return None

    def call_lua_function(self, lua_function_name: str, *args: Any) -> Any:
        """
        Calls a global Lua function.
        """
        loguru.logger.trace(f"Calling Lua function: {lua_function_name} with args: {args}")
        try:
            lua_func = self._lua_globals[lua_function_name]
            if lua_func is None:
                loguru.logger.error(f"Lua function '{lua_function_name}' not found.")
                return None
            return lua_func(*args)
        except lupa.LuaError as e:
            loguru.logger.error(f"LuaError calling function '{lua_function_name}': {e}")
            raise
        except Exception as e:
            loguru.logger.error(f"Unexpected error calling Lua function '{lua_function_name}': {e}")
            raise
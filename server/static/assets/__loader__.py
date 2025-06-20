# __loader__.py
import os
import loguru
from typing import TYPE_CHECKING

from utils.AppServices import AppServices

if TYPE_CHECKING:
    from utils.AssetBridge import LuaBridge

def load_lua_asset(file_path: str, lua_bridge: 'LuaBridge', asset_type: str):
    """
    Loads a single Lua asset file using the provided LuaBridge.
    The Lua script is expected to register itself or return its definition.
    """
    loguru.logger.info(f"Loading Lua asset: {file_path}")
    try:
        # Lua scripts can either register themselves by calling an exposed Python function
        # or return a table that Python can then process.
        # For now, we'll just execute the file. The Lua script needs to handle its registration.
        asset_definition = lua_bridge.execute_lua_file(file_path)
        
        if asset_definition: # This means the Lua script returned a value
            asset_name = None
            # Lupa tables can be accessed like attributes or using get()
            if hasattr(asset_definition, 'name'):
                asset_name = asset_definition.name
            elif callable(getattr(asset_definition, 'get', None)) and asset_definition.get('name'):
                asset_name = asset_definition.get('name')
            
            if asset_name:
                full_asset_key = f"{asset_type}.{asset_name}"
                loguru.logger.info(f"Registering returned Lua asset: Key='{full_asset_key}'")
                AppServices.asset_registry.register(full_asset_key, asset_definition)
                loguru.logger.debug(f"Lua asset '{file_path}' (Name: {asset_name}) registered as '{full_asset_key}'. Type: {type(asset_definition)}")
            else:
                loguru.logger.warning(f"Lua asset from {file_path} of type '{asset_type}' was returned but has no 'name' attribute/key. Cannot register automatically.")
        # If asset_definition is None, we assume the Lua script registered itself via an exposed function like 'register_asset'.
    except Exception as e: # Catching generic Exception as execute_lua_file can raise various errors
        loguru.logger.error(f"Error loading Lua asset from {file_path}: {e}")

def load_assets_from_directory(directory_path: str, lua_bridge: 'LuaBridge'):
    asset_subdir_name = os.path.basename(directory_path)
    loguru.logger.info(f"Scanning Lua assets in: {directory_path} (for type: {asset_subdir_name})")
    for filename in os.listdir(directory_path):
        if filename.endswith(".lua"): # Look for .lua files
            file_path = os.path.join(directory_path, filename)
            # Pass the asset_subdir_name so Lua knows what type of asset it's defining
            # or have a more robust registration system.
            load_lua_asset(file_path, lua_bridge, asset_subdir_name)

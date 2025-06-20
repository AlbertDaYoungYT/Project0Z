
import loguru
import os # Added for os.path.exists and os.path.join
from server.event import EventHandler
from server.event.server.ServerAssetLoadEvent import ServerAssetLoadEvent
from static.assets.__expose__ import default_expose
from utils.AssetBridge import LuaBridge # Assuming AssetBridge is the correct name
from utils.AppServices import AppServices # For accessing asset_registry
# Import decorators and core definitions directly
# from .__states__ import *
# from .__actions__ import *

# Assuming the loader is now designed for Lua assets primarily
from .__loader__ import load_assets_from_directory

asset_directories = [
    "effects",
    "status",

    # Core Game Concepts
    "abilities",
    "skills",
    "spells",
    "talents",
    "traits",
    "classes",
    "races",
    "factions",
    "guilds",

    # Character/Entity Attributes & Stats
    "attributes",
    "stats",

    # Combat & Mechanics
    "damage_types",
    "resistance_types",
    "vulnerability_types",
    "immunities",
    "conditions",
    "auras",
    "buffs",
    "debuffs",
    "enchants",

    # Item & Economy Related
    "gems",
    "tiers",
    "qualities",
    "rarities", # Item Rarity
    "durability",
    "currency",
    "inventory",
    "equipment",
    "bank",
    "auction_house",
    "vendors",
    "trainers",

    # Professions & Activities
    "professions",

    # World & Environment
    "entities",
    "items",
    "tiles",
    "sectors",
    "biomes",

    # Crafting & World Interaction
    "recipes",
    "structures",
    "quests",
    "dialogues",
    "loot_tables",
    "world_gen",

    # Visuals & Audio
    "ui",
    "animations",
    "particles",
    "shaders",
    "sounds",
    "templates"
]

def asset_load_listener(event: ServerAssetLoadEvent):
    loguru.logger.info("Asset load listener triggered. Initializing Lua bridge and loading Lua assets...")
    try:
        # It's generally better to have a single LuaBridge instance managed by AppServices
        # For this example, we'll create it here.
        lua_assets_root = "static/assets/lua" # Define a root for Lua assets

        # In a real app: lua_bridge = AppServices.get_lua_bridge()
        # Ensure LuaBridge is initialized with asset_root_path for correct module resolution
        lua_bridge = LuaBridge(asset_root_path=lua_assets_root)

        # --- Python to Lua Bridge Setup ---
        default_expose(lua_bridge)

        

        # Expose asset registration function to Lua
        def register_lua_asset(asset_type: str, asset_name: str, asset_data: dict): # Changed asset_table to asset_data
            loguru.logger.info(f"[Python Registry] Lua asset registration called: Type='{asset_type}', Name='{asset_name}'")
            full_asset_key = f"{asset_type}.{asset_name}"
            try:
                AppServices.asset_registry.register(full_asset_key, asset_data)
                loguru.logger.debug(f"Asset '{full_asset_key}' (from Lua call) stored in registry.")
            except Exception as e_reg:
                loguru.logger.error(f"Failed to register Lua asset '{full_asset_key}' via exposed function: {e_reg}")

        lua_bridge.expose_function_to_lua(register_lua_asset, "register_asset")

        # --- Load Lua Assets ---
        for directory_name in asset_directories:
            # Construct the full path to the Lua asset subdirectory
            full_lua_dir_path = os.path.join(lua_assets_root, directory_name)
            if os.path.exists(full_lua_dir_path) and os.path.isdir(full_lua_dir_path):
                load_assets_from_directory(full_lua_dir_path, lua_bridge)
            else:
                loguru.logger.warning(f"Lua asset directory not found or is not a directory, skipping: {full_lua_dir_path}")

    except Exception as e:
        loguru.logger.critical(f"Fatal error during asset loading with LuaBridge: {e}")
        # event.cancel() # Consider cancelling the event if it's critical

    loguru.logger.info("Asset loading process finished.")

from dataclasses import dataclass
import os

from utils.Vectors import Vector2d


@dataclass
class GameConstants(object):
    GIT_COMMITHASH: str = os.getenv("GIT_COMMITHASH", "")
    
    VERSION: str = os.getenv("VERSION", "")
    MIN_CLIENT_VERSION: tuple[int] = (0, 0, 1)
    VERSION_PARTS: tuple[int] = (0, 0, 1)

    MAX_PLAYERS: int = 100

    # Features enabled by the server #TODO: Add some more features
    SERVER_FEATURES_COMBAT: bool = True
    SERVER_FEATURES_TRADING: bool = True
    SERVER_FEATURES_SECTORS: bool = True
    SERVER_FEATURES_LOADOUTS: bool = True
    SERVER_FEATURES_DYNAMIC_WEATHER: bool = True
    SERVER_FEATURES_CROSSPLAY: bool = True
    SERVER_FEATURES_MATCHMAKING: bool = True
    SERVER_FEATURES_CLANS: bool = False
    SERVER_FEATURES_ACHIEVEMENTS: bool = True
    SERVER_FEATURES_LEADERBOARDS: bool = True
    SERVER_FEATURES_EVENTS: bool = True
    SERVER_FEATURES_MOD_SUPPORT: bool = False
    SERVER_FEATURES_CUSTOM_MAPS: bool = False
    SERVER_FEATURES_ANTI_CHEAT: bool = False


    # Other Game Constants
    START_POSITION: Vector2d = Vector2d(0, 0)


from dataclasses import dataclass
from uuid import UUID

from . import Model
from server.GameSession import GameSession
from utils.Vectors import Vector2d


@dataclass
class PlayerModel(Model):
    id: UUID
    account_id: UUID
    player_ship_id: UUID
    session_key: str

    player_location: Vector2d
    
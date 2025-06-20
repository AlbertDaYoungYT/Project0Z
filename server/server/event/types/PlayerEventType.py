from enum import Enum

from server.player.Player import Player
from .. import Event



class PlayerEvent(Event):
    def __init__(self, player: Player):
        super().__init__()
        self._player = player

    def get_server_type(self) -> Player:
        return self._player
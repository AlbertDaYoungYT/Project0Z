from typing import Optional

from .. import Cancellable
from ..types.PlayerEventType import PlayerEvent

from server.player.Player import Player


class PlayerChatEvent(PlayerEvent, Cancellable):
    def __init__(
        self,
        player: Player,
        message: str,
        to: Optional[Player] = None,
        channel_id: Optional[int] = None,
    ):
        super().__init__(player)
        self._message = message
        self._to = to
        self._channel_id = channel_id

    def get_message(self) -> str:
        return self._message

    def set_message(self, message: str):
        self._message = message

    def get_to(self) -> Optional[Player]:
        return self._to

    def set_to(self, to: Optional[Player]):
        self._to = to

    def get_channel_id(self) -> Optional[int]:
        return self._channel_id

    def set_channel_id(self, channel_id: Optional[int]):
        self._channel_id = channel_id

    def get_target_uid(self) -> int:
        return self._to.get_uid() if self._to else -1

    def get_message_as_int(self) -> int:
        try:
            return int(self._message)
        except ValueError:
            return -1

    def get_channel(self) -> int:
        return self._channel_id if self._channel_id is not None else -1
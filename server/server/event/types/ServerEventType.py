from enum import Enum

from .. import Event


class ServerEventType(Enum):
    INTERNAL = "INTERNAL"
    DISPATCH = "DISPATCH"
    GAME = "GAME"

class ServerEvent(Event):
    def __init__(self, type: ServerEventType):
        super().__init__()
        self._type = type

    def get_server_type(self) -> ServerEventType:
        return self._type
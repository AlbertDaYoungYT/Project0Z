from typing import Optional

from .. import Cancellable
from ..types.ServerEventType import ServerEvent, ServerEventType


class ServerAssetErrorEvent(ServerEvent, Cancellable):
    def __init__(self, message: str):
        self.message = message
        super().__init__(ServerEventType.INTERNAL)
    
    def get_message(self) -> str:
        return self.message
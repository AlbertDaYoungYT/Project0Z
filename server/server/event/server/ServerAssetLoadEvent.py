from typing import Optional

from .. import Cancellable
from ..types.ServerEventType import ServerEvent, ServerEventType


class ServerAssetLoadEvent(ServerEvent, Cancellable):
    def __init__(self):
        super().__init__(ServerEventType.INTERNAL)
    
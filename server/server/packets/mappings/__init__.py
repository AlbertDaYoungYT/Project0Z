
from dataclasses import dataclass
from typing import Callable, Optional

import loguru

from server.packets.BasePacket import ProtocolPacket
from utils.types.Errors import Codes, Error
from utils.types.Reasons import ProtocolReasons


@dataclass
class ProtocolResponse:
    pass


class PacketProtocolMap:


    def __init__(self):
        self.protocol_stage: int = 0
        self.protocol_map: dict[int, Callable[[int, Optional[int], Optional[bool]], ProtocolResponse]]
    
    def next(self) -> Error:
        if not self.protocol_stage < len(self.protocol_map.keys()):
            loguru.logger.warning(Codes.INDEX_ERROR.to_logger())
            return Codes.INDEX_ERROR
        
        self.protocol_stage += 1
        return self.get(stage=self.protocol_stage - 1)

    def get(self, stage: int = 0) -> Callable[[int, Optional[int], Optional[bool]], ProtocolResponse] | None:
        return self.protocol_map.get(stage)
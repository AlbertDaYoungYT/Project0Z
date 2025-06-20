

from server.GameSession import GameSession
from server.event.types.ServerEventType import ServerEvent, ServerEventType
from server.event import Cancellable


class ReceivePacketEvent(ServerEvent, Cancellable):
    def __init__(self, session: GameSession, opcode: int, header: bytes, payload: bytes):
        self.session = session
        self.opcode = opcode
        self.header = header
        self.payload = payload
        super().__init__(ServerEventType.INTERNAL)
    
    def get_session(self) -> GameSession:
        return self.session
    
    def get_opcode(self) -> int:
        return self.opcode
    
    def get_header(self) -> bytes:
        return self.header
    
    def get_payload(self) -> bytes:
        return self.payload
    
    def cancel(self):
        self.cancelled = True

    def is_cancelled(self) -> bool:
        return self.cancelled
    
    def set_session(self, session: GameSession):
        self.session = session
    
    def set_opcode(self, opcode: int):
        self.opcode = opcode

    def set_header(self, header: bytes):
        self.header = header

    def set_payload(self, payload: bytes):
        self.payload = payload
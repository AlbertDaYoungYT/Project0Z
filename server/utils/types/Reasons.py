
import base64
from enum import Enum
import secrets
from uuid import UUID

from server.packets.BasePacket import BasePacket
from server.packets.PacketOpcodes import PacketOpcodes
from utils.types.Errors import Error, Codes


class Reason(Error):
    id: UUID = UUID(secrets.token_hex(16))

    http_status: int = 0
    
    def to_response(self, e: Exception | None = None, **kwargs):
        packet = BasePacket(PacketOpcodes.SERVER_REASON)
        packet.set_data(base64.b64encode(self.to_json(indent=0).encode()))
        packet.set_header(base64.b64encode(self.id.bytes))
        return packet

class SocketCloseReason(Enum):
    FATAL_ERROR = Reason(code=1, name="FATAL_ERROR", message="The server terminated the connection due to a fatal error.")
    SERVER_STOPPING = Reason(code=2, name="SERVER_STOPPING", message="Server is shutting down.")


    CLIENT_ACCOUNT_BANNED = Reason.from_error(Codes.ACCOUNT_BANNED)



class ProtocolReasons(Enum):
    DEFAULT = Reason(code=1, name="DEFAULT", message="Protocol Default Reason, if you see this please contact the developers.")
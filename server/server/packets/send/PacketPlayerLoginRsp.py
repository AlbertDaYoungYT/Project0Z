from server.GameSession import GameSession
from server.packets.BasePacket import BasePacket
from server.packets.PacketOpcodes import PacketOpcodes

import hashlib


class PacketPlayerLoginRsp(BasePacket):
    opcode = PacketOpcodes.PLAYER_LOGIN_RESPONSE

    def __init__(self, session: GameSession):
        super().__init__(opcode=self.opcode)
        # Build response data based on session
        self.use_dispatch_key = True

        self.set_header(hashlib.md5(
            session.session_key.bytes
        ).digest())

        self.set_data(session.session_key.bytes)

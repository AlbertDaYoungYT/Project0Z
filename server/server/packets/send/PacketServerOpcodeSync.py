from server.GameSession import GameSession
from server.packets.BasePacket import BasePacket
from server.packets.PacketOpcodes import PacketOpcodes

import hashlib
import base64


class PacketServerOpcodeSync(BasePacket): # TODO: Fix this or rather finish it when the Packet System has been finalized.
    opcode = PacketOpcodes.SERVER_OPCODE_SYNC

    def __init__(self, session: GameSession):
        super().__init__(opcode=self.opcode)
        opcodes = PacketOpcodes.to_json(indent=0)
        self.use_dispatch_key = True

        self.set_header(hashlib.md5(
            session.session_key.bytes
        ).digest())

        self.set_data(base64.b64encode(
            opcodes.encode()
        ))
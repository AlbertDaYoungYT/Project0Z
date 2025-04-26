
from server.GameSession import GameSession
from server.packets.Opcodes import opcodes
from server.packets.PacketHandler import PacketHandler
from server.packets.PacketOpcodes import PacketOpcodes


@opcodes(value=PacketOpcodes.PingReq)
class HandlerPingReq(PacketHandler):
    async def handle(self, session: GameSession, header: bytes, payload: bytes):
        pass
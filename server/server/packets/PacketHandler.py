from server.GameSession import GameSession


class PacketHandler:
    async def handle(self, session: GameSession, header: bytes, payload: bytes):
        raise NotImplementedError("Subclasses must implement the handle method")
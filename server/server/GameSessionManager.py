from typing import Dict

import loguru
from server.GameSession import GameSession
from utils.types.Reasons import SocketCloseReason
from utils.AppServices import AppServices



class GameSessionManager:
    _sessions: Dict[tuple, GameSession] = {} # Using address tuple as key

    def __init__(self, services: AppServices):
        self.services = services

    def get_session(self, addr: tuple) -> GameSession | None:
        return self._sessions.get(addr)
    
    async def create_session(self, transport, addr: tuple) -> GameSession:
        if addr not in self._sessions:
            loguru.logger.info(f"Creating new session for {addr}")
            session = GameSession(transport, addr, self.services)
            tunnel = KcpTunnel(addr, transport) # Or your tunnel implementation
            await session.on_connected(tunnel)
            self._sessions[addr] = session
            return session
        else:
            loguru.logger.warning(f"Attempted to create session for existing address: {addr}")
            return self._sessions[addr]

    async def on_connected(self, transport, addr):
        loguru.logger.info(f"New connection from {addr}")
        # In asyncio UDP, each received packet is a new "connection" in a sense
        # You might need a way to identify sessions based on client address
        if addr not in self._sessions:
            session = GameSession(transport, addr, self.services)
            tunnel = KcpTunnel(addr, transport) # Assuming direct UDP for now
            await session.on_connected(tunnel)
            self._sessions[addr] = session
        else:
            loguru.logger.warning(f"Session already exists for {addr}")

# Uncommented as its handled by the GameServerPacketHandler.py
#
#    async def handle_receive(self, data: bytes, addr: tuple):
#        session = self.get_session(addr)
#        if session:
#            await session.handle_receive(data)
#        else:
#            loguru.logger.warning(f"Received data for non-existent session at {addr}")

    async def handle_close(self, addr: tuple):
        if addr in self._sessions:
            session = self._sessions.pop(addr)
            await session.handle_close()
        else:
            loguru.logger.warning(f"Attempted to close non-existent session at {addr}")

    async def send_to_session(self, addr: tuple, data: bytes):
        session = self.get_session(addr)
        if session:
            await session.send_data(data)
        else:
            loguru.logger.warning(f"Cannot send to non-existent session at {addr}")
    
    async def stop(self):
        for addr, session in self._sessions.items():
            await session.close(reason=SocketCloseReason.SERVER_STOPPING)


class KcpTunnel:
    def __init__(self, addr, transport):
        self.addr = addr
        self.transport = transport
        # Placeholder for srtt (smoothed round-trip time)
        self.srtt_value = 0

    def get_address(self):
        return self.addr

    async def write_data(self, data: bytes):
        loguru.logger.info(f"KcpTunnel writing data to {self.addr}: {data.hex()}")
        if self.transport:
            self.transport.sendto(data, self.addr)

    async def close(self):
        loguru.logger.info(f"KcpTunnel closing connection to {self.addr}")
        if self.transport:
            self.transport.close() # Depending on asyncio usage

    def get_srtt(self):
        return self.srtt_value # Placeholder
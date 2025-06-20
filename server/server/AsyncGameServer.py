import asyncio
import struct

import loguru
from server.GameServerPacketHandler import GameServerPacketHandler
from server.GameSessionManager import GameSessionManager
from server.packets.PacketHandler import PacketHandler
from server.packets.PacketOpcodes import PacketOpcodes
from server.packets.PacketUtils import decode_packet_data, decode_packet_opcode
from utils.AppServices import AppServices


class AsyncGameServer:
    def __init__(self, host, port, services: AppServices):
        self.host = host
        self.port = port
        self.transport: asyncio.DatagramTransport = None
        self.protocol = None
        self.session_manager = GameSessionManager(services)
        self.packet_handler = GameServerPacketHandler(PacketHandler, services) 

        self.services = services

    async def handle_datagram(self, data: bytes, addr):
        loguru.logger.debug(data)
        if len(data) >= 4: # Assuming opcode (2 bytes) and header length (2 bytes)
            #opcode = struct.unpack('>H', data[:2])[0]
            #header_length = struct.unpack('>I', data[2:6])[0]
            #header = data[6 : 6 + header_length]
            #payload = data[6 + header_length :]
            packet_type, opcode, header, payload = decode_packet_data(data)
            loguru.logger.debug(f"{opcode}, {len(header)}, {header}, {payload}")

            session = self.session_manager.get_session(addr)
            if session:
                await self.packet_handler.handle(session, opcode, header, payload)
            else:
                loguru.logger.warning(f"Received packet with opcode {opcode} from unknown session at {addr}")
                # Handle initial connection/login packets here to create a session
                if await self._handle_initial_packets(data, addr):
                    session = self.session_manager.get_session(addr)
                    if session:
                        await self.packet_handler.handle(session, opcode, header, payload)

        else:
            loguru.logger.warning(f"Received too short data from {addr}")


    async def _handle_initial_packets(self, data: bytes, addr: tuple) -> bool:
        if len(data) >= 2:
            opcode = decode_packet_opcode(data)
            
            if opcode == PacketOpcodes.PING_REQUEST:
                await self.session_manager.create_session(self.transport, addr)
                return True
            if opcode == PacketOpcodes.PLAYER_LOGIN_REQUEST:
                await self.session_manager.create_session(self.transport, addr)
                return True
            # Add other initial packet handling here (e.g., token request)
        return False

    def connection_made(self, transport):
        self.transport = transport
        loguru.logger.info(f'Server started on udp://{self.host}:{self.port}')

    def connection_lost(self, exc):
        loguru.logger.info(f'Server socket closed "{exc}"')

    def datagram_received(self, data, addr):
        asyncio.create_task(self.handle_datagram(data, addr))
    
    async def stop(self):
        await self.session_manager.stop()
        self.transport.close()
    
    async def start(self):
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=(self.host, self.port)
        )

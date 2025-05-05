
from dataclasses import dataclass
import secrets
import struct
from uuid import UUID
import loguru

import loguru
from server.packets.BasePacket import BasePacket
from connectors import PlayerAccountConnector
from server.states.SessionState import SessionState
from utils import Crypto
from utils.DatabaseAdapter import Serializable


@dataclass
class GameSession(Serializable):
    session_key: UUID
    transport: object
    addr: object
    player_account_connector: PlayerAccountConnector.Connector
    state: SessionState

    client_time: float
    client_last_ping_time: float



    def __init__(self, transport, addr, services):
        self.session_key = UUID(secrets.token_hex(16))
        self.transport = transport
        self.addr = addr
        self.state = SessionState.WAITING_FOR_LOGIN

        self.client_time = 0.0
        self.client_last_ping_time = 0.0

        self.services = services

    def register_session(self, player, account):
        self.player_account_connector = PlayerAccountConnector.Connector(player, account)
        self.state = SessionState.WAITING_FOR_TOKEN

    async def on_connected(self, tunnel):
        loguru.logger.info(f"GameSession connected with tunnel to {self.addr}")
        self.tunnel = tunnel
        # Perform any initial setup for the session

    async def handle_receive(self, data: bytes):
        loguru.logger.info(f"GameSession received data from {self.addr}: {data.hex()}")
        # Process the received game data

        try:
            # Basic packet parsing (adjust based on your needs)
            if len(data) >= 2:
                opcode = struct.unpack('>H', data[0:2])[0]
                header_length = struct.unpack('>H', data[2:4])[0]
                header = data[4 : 4 + header_length]
                payload = data[4 + header_length :] # Assuming payload is after opcode and header

                if opcode in self.handlers:
                    handler = self.handlers[opcode]
                    await handler.handle(self, header, payload)
                else:
                    loguru.logger.warning(f"No handler found for opcode: {opcode}")
            else:
                loguru.logger.warning("Received too short data for opcode.")

        except Exception as e:
            loguru.logger.error(f"Error handling datagram: {e}")

    async def handle_close(self):
        loguru.logger.info(f"GameSession closed for {self.addr}")
        # Perform cleanup for the session

    async def send(self, data: BasePacket):
        try:
            packet: bytes = data.build()
            #if data.should_encrypt: packet = Crypto.xor(packet, ConfigContainer.dispatchKey).encode("utf-8")

            loguru.logger.info(f"GameSession sending data to {self.addr}: {packet.hex()}")
            if self.transport:
                self.transport.sendto(packet, self.addr)
        except Exception as e:
            loguru.logger.debug(f"Unable to send packet to client. {e}")

    async def close(self):
        loguru.logger.info(f"Closing GameSession for {self.addr}")
        if self.transport:
            self.transport.close() # Depending on asyncio usage, this might need adjustment

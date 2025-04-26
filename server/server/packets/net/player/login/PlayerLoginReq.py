import struct

import loguru


class PlayerLoginReq:
    def __init__(self, token: str):
        self.token = token

    @staticmethod
    def parse_from(payload: bytes):
        # This is a placeholder - implement actual parsing based on your protocol
        try:
            token_length = struct.unpack('>H', payload[2:4])[0]  # Example: first 4 bytes are token length
            token = payload[4 : 4 + token_length].decode('utf-8')
            loguru.logger.debug(f"{token_length}, {token}, {payload}")
            return PlayerLoginReq(token=token)
        except Exception as e:
            loguru.logger.error(f"Error parsing PlayerLoginReq: {e}")
            return None
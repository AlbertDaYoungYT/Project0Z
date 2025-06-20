
from enum import Enum
import struct

from server.packets.Opcodes import OpcodeMeta



class PacketType(Enum):
    BASE_PACKET: bytes = b"\x00"
    PROTOCOL_PACKET: bytes = b"\x01"


class BasePacket(metaclass=OpcodeMeta):
    opcode = None
    disabled = False
    
    def __init__(self, opcode: int, build_header: bool = False):
        self.packet_type = PacketType.BASE_PACKET
        self.should_encrypt: bool = True
        self.opcode: int = opcode
        self.should_build_header: bool = build_header
        self.header: bytes = b''
        self.data: bytes = b''
        self.use_dispatch_key: bool = False


    def get_opcode(self): return self.opcode
    def set_opcode(self, opcode: int): self.opcode = opcode

    def get_use_dispatch_key(self): return self.use_dispatch_key
    def set_use_dispatch_key(self, use_dispatch_key: bool): self.use_dispatch_key = use_dispatch_key

    def get_header(self): return self.header
    def set_header(self, header: bytes): self.header = header

    def get_data(self): return self.data
    def set_data(self, data: bytes): self.data = data

    def build(self) -> bytes:
        if self.header is None:
            self.header = b''
        if self.data is None:
            self.data = b''

        buffer = bytearray()

        # Write Packet type (unsigned short, 2 bytes)
        buffer.extend(struct.pack('>H', self.packet_type))

        # Write opcode (unsigned short, 2 bytes)
        buffer.extend(struct.pack('>H', self.opcode))

        # Write header length (unsigned short, 2 bytes)
        buffer.extend(struct.pack('>H', len(self.header)))

        # Write data length (unsigned int, 4 bytes)
        buffer.extend(struct.pack('>I', len(self.data)))

        # Write header bytes
        buffer.extend(self.header)

        # Write data bytes
        buffer.extend(self.data)

        return bytes(buffer)
    


class ProtocolPacket(BasePacket):

    def __init__(self, opcode: int, stage_id: int = 0, build_header: bool = False):
        self.stage_id: int = stage_id
        super().__init__(opcode, build_header)

        self.packet_type = PacketType.PROTOCOL_PACKET

    def build(self):
        if self.header is None:
            self.header = b''
        if self.data is None:
            self.data = b''
        
        header_buffer = bytearray()

        header_buffer.extend(struct.pack('>H', self.stage_id))
        header_buffer.extend(self.header)

        self.set_header(bytes(header_buffer))

        return super().build()
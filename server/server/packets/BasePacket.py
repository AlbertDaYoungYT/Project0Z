


import struct

from server.packets.Opcodes import OpcodeMeta


class BasePacket(metaclass=OpcodeMeta):
    opcode = None
    disabled = False
    
    def __init__(self, opcode: int, build_header: bool = False):
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
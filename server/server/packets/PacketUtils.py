

import struct

from server.packets.BasePacket import BasePacket


def decode_packet_opcode(data: bytes) -> int:
    return struct.unpack('>H', data[:2])[0]

def decode_packet_data(data: bytes) -> tuple:
    packet_type = struct.unpack('>H', data[:2])[0]
    opcode = struct.unpack('>H', data[2:4])[0]

    header_length = struct.unpack('>I', data[4:8])[0]

    header = data[8 : 8 + header_length]
    payload = data[8 + header_length :]

    return packet_type, opcode, header, payload

def decode_packet_data_2_json(data: bytes) -> dict:
    packet_type, opcode, header, payload = decode_packet_data(data)

    return {
        'packet_type': packet_type,
        'opcode': opcode,
        'header': header.decode('utf-8'),
        'payload': payload.decode('utf-8')
    }

def decode_packet_data_2_class(data: bytes) -> BasePacket:
    packet_type, opcode, header, payload = decode_packet_data(data)

    packet = BasePacket(opcode)
    packet.set_header(header)
    packet.set_payload(payload)

    packet.packet_type = packet_type

    return packet
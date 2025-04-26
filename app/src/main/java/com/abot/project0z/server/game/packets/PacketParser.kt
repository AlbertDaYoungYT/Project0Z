package com.abot.project0z.server.game.packets

import java.io.ByteArrayInputStream
import java.nio.ByteBuffer
import kotlin.concurrent.read
import kotlin.text.toLong

class PacketParser {

    fun parse(packet: ByteArray): BasePacket? {
        if (packet.size < 8) { // Minimum size for opcode, header size, and data size
            return null
        }

        val bais = ByteArrayInputStream(packet)

        return try {
            val opcode = readUint16(bais)
            val headerSize = readUint16(bais)
            val dataSize = readUint32(bais)

            if (packet.size < 8 + headerSize + dataSize) {
                return null // Incomplete packet
            }

            val header = readBytes(bais, headerSize)
            val data = readBytes(bais, dataSize.toInt()) // Ensure dataSize is Int

            val packet: BasePacket = BasePacket(opcode)
            packet.setHeader(header)
            packet.setData(data)
            packet
        } catch (e: Exception) {
            null // Parsing error
        }
    }

    private fun readUint16(bais: ByteArrayInputStream): Int {
        val buffer = ByteArray(2)
        if (bais.read(buffer) != 2) {
            throw Exception("Could not read 2 bytes")
        }
        return ByteBuffer.wrap(buffer).short.toInt() and 0xFFFF // Convert Short to unsigned Int
    }

    private fun readUint32(bais: ByteArrayInputStream): Long {
        val buffer = ByteArray(4)
        if (bais.read(buffer) != 4) {
            throw Exception("Could not read 4 bytes")
        }
        return ByteBuffer.wrap(buffer).int.toLong() and 0xFFFFFFFFL // Convert Int to unsigned Long
    }

    private fun readBytes(bais: ByteArrayInputStream, count: Int): ByteArray {
        val buffer = ByteArray(count)
        if (bais.read(buffer) != count) {
            throw Exception("Could not read $count bytes")
        }
        return buffer
    }
}

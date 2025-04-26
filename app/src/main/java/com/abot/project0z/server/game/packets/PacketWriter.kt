package com.abot.project0z.server.game.packets

import java.io.ByteArrayOutputStream
import java.io.IOException


class PacketWriter {
    // Little endian
    private val baos = ByteArrayOutputStream(128)

    fun build(): ByteArray {
        return baos.toByteArray()
    }

    // Writers
    fun writeEmpty(i: Int) {
        var i = i
        while (i > 0) {
            baos.write(0)
            i--
        }
    }

    fun writeMax(i: Int) {
        var i = i
        while (i > 0) {
            baos.write(0xFF)
            i--
        }
    }

    fun writeInt8(b: Byte) {
        baos.write(b.toInt())
    }

    fun writeInt8(i: Int) {
        baos.write(i.toByte().toInt())
    }

    fun writeBoolean(b: Boolean) {
        baos.write(if (b) 1 else 0)
    }

    fun writeUint8(b: Byte) {
        // Unsigned byte
        baos.write(b.toInt() and 0xFF)
    }

    fun writeUint8(i: Int) {
        baos.write(i.toByte().toInt() and 0xFF)
    }

    fun writeUint16(i: Int) {
        // Unsigned short
        baos.write((i and 0xFF).toByte().toInt())
        baos.write(((i ushr 8) and 0xFF).toByte().toInt())
    }

    fun writeUint24(i: Int) {
        // 24 bit integer
        baos.write((i and 0xFF).toByte().toInt())
        baos.write(((i ushr 8) and 0xFF).toByte().toInt())
        baos.write(((i ushr 16) and 0xFF).toByte().toInt())
    }

    fun writeInt16(i: Int) {
        // Signed short
        baos.write(i.toByte().toInt())
        baos.write((i ushr 8).toByte().toInt())
    }

    fun writeUint32(i: Int) {
        // Unsigned int
        baos.write((i and 0xFF).toByte().toInt())
        baos.write(((i ushr 8) and 0xFF).toByte().toInt())
        baos.write(((i ushr 16) and 0xFF).toByte().toInt())
        baos.write(((i ushr 24) and 0xFF).toByte().toInt())
    }

    fun writeInt32(i: Int) {
        // Signed int
        baos.write(i.toByte().toInt())
        baos.write((i ushr 8).toByte().toInt())
        baos.write((i ushr 16).toByte().toInt())
        baos.write((i ushr 24).toByte().toInt())
    }

    fun writeUint32(i: Long) {
        // Unsigned int (long)
        baos.write((i and 0xFFL).toByte().toInt())
        baos.write(((i ushr 8) and 0xFFL).toByte().toInt())
        baos.write(((i ushr 16) and 0xFFL).toByte().toInt())
        baos.write(((i ushr 24) and 0xFFL).toByte().toInt())
    }

    fun writeFloat(f: Float) {
        this.writeUint32(java.lang.Float.floatToRawIntBits(f))
    }

    fun writeUint64(l: Long) {
        baos.write((l and 0xFFL).toByte().toInt())
        baos.write(((l ushr 8) and 0xFFL).toByte().toInt())
        baos.write(((l ushr 16) and 0xFFL).toByte().toInt())
        baos.write(((l ushr 24) and 0xFFL).toByte().toInt())
        baos.write(((l ushr 32) and 0xFFL).toByte().toInt())
        baos.write(((l ushr 40) and 0xFFL).toByte().toInt())
        baos.write(((l ushr 48) and 0xFFL).toByte().toInt())
        baos.write(((l ushr 56) and 0xFFL).toByte().toInt())
    }

    fun writeDouble(d: Double) {
        val l = java.lang.Double.doubleToLongBits(d)
        this.writeUint64(l)
    }

    fun writeString16(s: String?) {
        if (s == null) {
            this.writeUint16(0)
            return
        }

        this.writeUint16(s.length * 2)
        for (i in 0 until s.length) {
            val c = s[i]
            this.writeUint16(c.code.toShort().toInt())
        }
    }

    fun writeString8(s: String?) {
        if (s == null) {
            this.writeUint16(0)
            return
        }

        this.writeUint16(s.length)
        for (i in 0 until s.length) {
            val c = s[i]
            this.writeUint8(c.code.toByte())
        }
    }

    fun writeDirectString8(s: String?, expectedSize: Int) {
        if (s == null) {
            return
        }

        for (i in 0 until expectedSize) {
            val c = if (i < s.length) s[i] else 0.toChar()
            this.writeUint8(c.code.toByte())
        }
    }

    fun writeBytes(bytes: ByteArray?) {
        try {
            baos.write(bytes)
        } catch (e: IOException) {
            // TODO Auto-generated catch block
            e.printStackTrace()
        }
    }

    fun writeBytes(bytes: IntArray) {
        val b = ByteArray(bytes.size)
        for (i in bytes.indices) b[i] = bytes[i].toByte()

        try {
            baos.write(b)
        } catch (e: IOException) {
            // TODO Auto-generated catch block
            e.printStackTrace()
        }
    }
}

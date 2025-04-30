package com.abot.project0z.server.game.packets

import android.annotation.SuppressLint
import java.io.ByteArrayOutputStream
import java.io.IOException


public class BasePacket {
    var shouldEncrypt: Boolean = true
    private var opcode = 0
    private var shouldBuildHeader = false
    private lateinit var header: ByteArray
    private lateinit var data: ByteArray

    // Encryption
    private var useDispatchKey = false

    constructor(opcode: Int) {
        this.opcode = opcode
    }

    constructor(opcode: Int, buildHeader: Boolean) {
        this.opcode = opcode
        this.shouldBuildHeader = buildHeader
    }

    fun getOpcode(): Int {
        return opcode
    }

    fun setOpcode(opcode: Int) {
        this.opcode = opcode
    }

    fun useDispatchKey(): Boolean {
        return useDispatchKey
    }

    fun setUseDispatchKey(useDispatchKey: Boolean) {
        this.useDispatchKey = useDispatchKey
    }

    fun getHeader(): ByteArray? {
        return header
    }

    fun setHeader(header: ByteArray) {
        this.header = header
    }

    fun shouldBuildHeader(): Boolean {
        return shouldBuildHeader
    }

    fun getData(): ByteArray? {
        return data
    }

    fun setData(data: ByteArray) {
        this.data = data
    }

    fun build(): ByteArray {
        if (getHeader() == null) {
            this.header = ByteArray(0)
        }

        if (getData() == null) {
            this.data = ByteArray(0)
        }

        val baos =
            ByteArrayOutputStream(2 + 2 + 2 + 4 + getHeader()!!.size + getData()!!.size + 2)

        this.writeUint16(baos, opcode)
        this.writeUint16(baos, header.size)
        this.writeUint32(baos, data.size)
        this.writeBytes(baos, header)
        this.writeBytes(baos, data)

        return baos.toByteArray()
    }

    fun writeUint16(baos: ByteArrayOutputStream, i: Int) {
        // Unsigned short
        baos.write(((i ushr 8) and 0xFF).toByte().toInt())
        baos.write((i and 0xFF).toByte().toInt())
    }

    fun writeUint32(baos: ByteArrayOutputStream, i: Int) {
        // Unsigned int (long)
        baos.write(((i ushr 24) and 0xFF).toByte().toInt())
        baos.write(((i ushr 16) and 0xFF).toByte().toInt())
        baos.write(((i ushr 8) and 0xFF).toByte().toInt())
        baos.write((i and 0xFF).toByte().toInt())
    }

    fun writeBytes(baos: ByteArrayOutputStream, bytes: ByteArray?) {
        try {
            baos.write(bytes)
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }
}
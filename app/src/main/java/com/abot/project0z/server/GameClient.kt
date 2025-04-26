package com.abot.project0z.server;

import androidx.compose.ui.semantics.disabled
import com.abot.project0z.MainActivity
import com.abot.project0z.server.game.GameSession
import com.abot.project0z.server.game.packets.BasePacket
import com.abot.project0z.server.game.packets.Opcodes
import com.abot.project0z.server.game.packets.PacketHandler
import com.abot.project0z.server.game.packets.PacketParser
import kotlinx.coroutines.*
import java.io.*
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetSocketAddress
import java.nio.ByteBuffer
import java.nio.ByteOrder


@OptIn(ExperimentalStdlibApi::class)
class GameClient(private val host: String, private val port: Int) {
    private val session: GameSession? = null
    private var socket: DatagramSocket? = null
    private var receiveJob: Job? = null
    private val handlers: MutableMap<Int, PacketHandler> = mutableMapOf()

    fun connect() {
        socket = DatagramSocket()
        println("Connected to server at $host:$port")
        startReceiving()
    }

    fun registerPacketHandler(handlerClass: Class<out PacketHandler?>) {
        try {
            val opcode: Opcodes = handlerClass.getAnnotation(Opcodes::class.java) ?: return
            if (opcode.disabled || opcode.value <= 0) {
                return
            }

            val packetHandler = handlerClass.getDeclaredConstructor().newInstance()
            packetHandler?.let { this.handlers.put(opcode.value, it) }
        } catch (e: java.lang.Exception) {
            MainActivity.getLogger()
                .warn("Unable to register handler ${handlerClass.simpleName}. Reason = $e")
        }
    }

    fun registerHandlers(handlerClass: Class<out PacketHandler?>) {
        val handlerClasses: MutableSet<out Class<out PacketHandler?>>? = MainActivity.reflector.getSubTypesOf(handlerClass)
        if (handlerClasses != null) {
            for (obj in handlerClasses) {
                this.registerPacketHandler(obj)
            }
        }

        // Debug
        MainActivity.getLogger()
            .info("Registered " + this.handlers.size.toString() + " " + handlerClass.simpleName + "s")
    }

    private fun startReceiving() {
        receiveJob = CoroutineScope(Dispatchers.IO).launch {
            val buffer = ByteArray(1024) // Adjust buffer size as needed
            val packet = DatagramPacket(buffer, buffer.size)
            while (isActive && socket?.isClosed == false) {
                try {
                    socket?.receive(packet)
                    val receivedData = packet.data.copyOfRange(0, packet.length)
                    println("Received: ${receivedData.toHexString()} from ${packet.socketAddress}")
                    // Process received data here
                    handleReceivedData(receivedData)
                } catch (e: Exception) {
                    if (isActive) {
                        println("Error receiving data: ${e.message}")
                    }
                }
            }
        }
    }

    private fun handleReceivedData(data: ByteArray) {
        // Example: Print the received data as a hex string
        println("Handling received data: ${data.toHexString()}")
        // Add your logic to parse and process the data based on your server's protocol
        val parsedPacket: BasePacket = PacketParser().parse(data) ?: return
        val handler: PacketHandler = this.handlers.get(parsedPacket.getOpcode()) ?: return

        handler.handle(this.session, parsedPacket.getHeader(), parsedPacket.getData())
    }

    fun sendPacket(opcode: Short, header: ByteArray = ByteArray(0), payload: ByteArray = ByteArray(0)) {
        val opcodeBytes = ByteBuffer.allocate(2).order(ByteOrder.BIG_ENDIAN).putShort(opcode).array()
        val headerLengthBytes = ByteBuffer.allocate(4).order(ByteOrder.BIG_ENDIAN).putInt(header.size).array()
        val packet = opcodeBytes + headerLengthBytes + header + payload

        val address = InetSocketAddress(host, port)
        val datagramPacket = DatagramPacket(packet, packet.size, address)
        try {
            socket?.send(datagramPacket)
            println("Sent: ${packet.toHexString()}")
        } catch (e: Exception) {
            println("Error sending packet: ${e.message}")
        }
    }

    fun sendPacket(packet: BasePacket) {
        val packetData: ByteArray = packet.build()

        val address = InetSocketAddress(host, port)
        val datagramPacket = DatagramPacket(packetData, packetData.size, address)
        try {
            socket?.send(datagramPacket)
            println("Sent: ${packetData.toHexString()}")
        } catch (e: Exception) {
            println("Error sending packet: ${e.message}")
        }
    }

    fun close() {
        receiveJob?.cancel()
        socket?.close()
        println("Connection closed")
    }
}
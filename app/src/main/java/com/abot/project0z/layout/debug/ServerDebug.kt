package com.abot.project0z.layout.debug

import android.util.Log
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.abot.project0z.server.game.packets.BasePacket
import com.abot.project0z.server.game.packets.PacketParser
import com.abot.project0z.utils.Codes
import com.abot.project0z.viewmodels.errors.ErrorView
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.jsonObject
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.HttpURLConnection
import java.net.InetAddress
import java.net.SocketTimeoutException
import java.net.URL
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.security.MessageDigest
import kotlin.collections.contentToString
import kotlin.text.toByteArray

fun String.toMD5Hash(): String {
    val bytes = toByteArray()
    val md = MessageDigest.getInstance("MD5")
    val digest = md.digest(bytes)
    return digest.fold("", { str, it -> str + "%02x".format(it) })
}

@Composable
fun ServerDebug(modifier: Modifier = Modifier) {
    var responseData by remember { mutableStateOf("") }
    val coroutineScope = rememberCoroutineScope()
    var udpResponse by remember { mutableStateOf("") }

    Column(
        modifier = modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Button(onClick = {
            coroutineScope.launch {
                val jsonData = JSONObject().apply {
                    put("username", "AlbertDaYoung")
                    put("email", "kcobain465@gmail.com")
                    put("pwd_hash", "Really Secure Password".toMD5Hash())
                    // Add more key-value pairs as needed
                }
                responseData = loginToServer("http://192.168.1.2:8080", jsonData)
            }
        }) {
            Text("Login to Server")
        }
        Button(onClick = {
            coroutineScope.launch {
                val jsonData = JSONObject().apply {
                    put("username", "AlbertDaYoung")
                    put("email", "kcobain465@gmail.com")
                    put("pwd_hash", "Really Secure Password".toMD5Hash())
                    // Add more key-value pairs as needed
                }
                responseData = signupForServer("http://192.168.1.2:8080", jsonData)
            }
        }) {
            Text("Signup for Server")
        }
        Button(onClick = {
            coroutineScope.launch {
                val opcode = 101
                val tokenElement: JsonElement? = try {
                    Json.parseToJsonElement(responseData).jsonObject["token"]
                } catch (e: Exception) {
                    Log.e("UDP", "Error extracting token: ${e.message}", e)
                    null
                }

                if (tokenElement == null) {
                    udpResponse = "Error: Could not extract token from response."
                } else {
                    val tokenString = tokenElement.toString().replace("\"", "")
                    Log.d("UDP", "Extracted token: $tokenString")

                    val receivedBytes = sendAndReceiveBasePacketUdp(
                        "192.168.1.2",
                        23899,
                        opcode,
                        tokenString // Pass the token directly
                    )
                    udpResponse = if (receivedBytes != null) {
                        "Received: opcode = ${receivedBytes.getOpcode().toString()} header = ${receivedBytes.getHeader().toString()} payload = ${receivedBytes.getData().toString()}"
                    } else {
                        "No response or error."
                    }
                }
            }
        }) {
            Text("Send BasePacket")
        }

        if (udpResponse.isNotEmpty()) {
            Text(udpResponse)
        }

        if (responseData.isNotEmpty()) {
            Text("Response: $responseData")
        }

        Button(
            onClick = {
                ErrorView.showError(Codes.SUCCESS.details)
            }
        ) {
            Text("Throw Error")
        }
    }
}

suspend fun loginToServer(serverUrl: String, jsonData: JSONObject): String {
    return try {
        Log.d("Network", "Attempting to connect to: $serverUrl/signup")
        val url = URL("$serverUrl/login")
        withContext(Dispatchers.IO) {
            val connection = url.openConnection() as HttpURLConnection
            try {
                connection.requestMethod = "POST"
                connection.doOutput = true
                connection.setRequestProperty("Content-Type", "application/json")

                val outputStreamWriter = OutputStreamWriter(connection.outputStream)
                outputStreamWriter.write(jsonData.toString())
                outputStreamWriter.flush()
                outputStreamWriter.close()

                val reader = BufferedReader(InputStreamReader(connection.inputStream))
                val response = StringBuilder()
                var line = reader.readLine()
                while (line != null) {
                    response.append(line)
                    line = reader.readLine()
                }
                reader.close()
                Log.d("Network", "Successfully received response: $response")
                Codes.SUCCESS.details.show()
                response.toString()
            } finally {
                connection.disconnect()
            }
        }
    } catch (e: Exception) {
        Codes.INTERNAL_SERVER_ERROR.details.show()
        Log.e("Network", "Error posting data to $serverUrl/login: ${e.message}", e)
        "Error: ${e.message}"
    }
}

suspend fun signupForServer(serverUrl: String, jsonData: JSONObject): String {
    return try {
        Log.d("Network", "Attempting to connect to: $serverUrl/signup")
        val url = URL("$serverUrl/signup")
        withContext(Dispatchers.IO) {
            val connection = url.openConnection() as HttpURLConnection
            try {
                connection.requestMethod = "POST"
                connection.doOutput = true
                connection.setRequestProperty("Content-Type", "application/json")

                val outputStreamWriter = OutputStreamWriter(connection.outputStream)
                outputStreamWriter.write(jsonData.toString())
                outputStreamWriter.flush()
                outputStreamWriter.close()

                val reader = BufferedReader(InputStreamReader(connection.inputStream))
                val response = StringBuilder()
                var line = reader.readLine()
                while (line != null) {
                    response.append(line)
                    line = reader.readLine()
                }
                reader.close()
                Log.d("Network", "Successfully received response: $response")
                Codes.SUCCESS.details.show()
                response.toString()
            } finally {
                connection.disconnect()
            }
        }
    } catch (e: Exception) {
        Codes.INTERNAL_SERVER_ERROR.details.show()
        Log.e("Network", "Error posting data to $serverUrl/login: ${e.message}", e)
        "Error: ${e.message}"
    }
}

suspend fun sendAndReceiveBasePacketUdp(
    serverAddress: String,
    serverPort: Int,
    opcode: Int,
    token: String,
    receiveTimeoutMillis: Int = 5000,
    maxReceiveSize: Int = 1024
): BasePacket? = withContext(Dispatchers.IO) {
    try {
        val tokenBytes = token.toByteArray(Charsets.UTF_8)
        val tokenLength = tokenBytes.size

        // 1. Correctly prepare the data payload: Token length (2 bytes) + Token (UTF-8 bytes)
        val dataBuffer = ByteBuffer.allocate(2 + tokenLength).order(ByteOrder.BIG_ENDIAN)
        dataBuffer.putShort(tokenLength.toShort()) // Token length as short
        dataBuffer.put(tokenBytes) // Token bytes
        val data = dataBuffer.array()

        // 2. Header (empty)
        val header = ByteArray(0)

        // 3. Build the complete packet: Opcode (2) + Header Length (2) + Data Length (4) + Data (no header)
        val packetLength = 2 + 2 + 4 + data.size // Correctly calculate packet length
        val buffer = ByteBuffer.allocate(packetLength) // Use the calculated length
        buffer.order(ByteOrder.BIG_ENDIAN)
        buffer.putShort(opcode.toShort())
        buffer.putShort(0) // Correctly set header length to 0
        buffer.putInt(data.size)
        buffer.put(data) // Only put data, as header is empty
        val packetBytes = buffer.array()

        Log.d("UDP", "Calculated packet length: $packetLength")
        Log.d("UDP", "Token length: $tokenLength")
        Log.d("UDP", "Packet bytes (length: ${packetBytes.size}): ${packetBytes.contentToString()}")

        // 4. Send and receive (same as before)
        val socket = DatagramSocket()
        socket.soTimeout = receiveTimeoutMillis
        val address = InetAddress.getByName(serverAddress)
        val sendPacket = DatagramPacket(packetBytes, packetBytes.size, address, serverPort)
        socket.send(sendPacket)

        Log.d("UDP", "BasePacket sent successfully. Waiting for response...")

        val receiveBuffer = ByteArray(maxReceiveSize)
        val receivePacket = DatagramPacket(receiveBuffer, receiveBuffer.size)
        socket.receive(receivePacket)

        socket.close()

        val receivedData = receivePacket.data.copyOfRange(0, receivePacket.length)
        val receivedPacket = PacketParser().parse(receivedData)
        Log.d("UDP", "Received response (length: ${receivedData.size}): ${receivedData.contentToString()}")
        receivedPacket
    } catch (e: SocketTimeoutException) {
        Log.w("UDP", "Timeout waiting for response from server.")
        null
    } catch (e: Exception) {
        Log.e("UDP", "Error sending/receiving BasePacket: ${e.message}", e)
        null
    }
}
package com.abot.project0z.server.game.packets.net.player.login

import com.abot.project0z.MainActivity
import com.abot.project0z.utils.Codes
import com.abot.project0z.utils.hashByteArray
import com.abot.project0z.utils.verifyByteArray

class PlayerLoginRsp(
    public val sessionKey: String? = null
) {

    companion object {
        fun parse_from(header: ByteArray, payload: ByteArray): PlayerLoginRsp? {
            try {
                if (verifyByteArray(payload, header)) {
                    return PlayerLoginRsp(sessionKey=payload.toString())
                }
                MainActivity.getLogger().warn(Codes.INVALID_TOKEN.details.toLogger())
                throw VerifyError("Error validating token from server, expected hash = ${hashByteArray(payload).toString()} got hash = ${header.toString()}")
            } catch (e: Exception) {
                MainActivity.getLogger().warn("Error parsing in PlayerLoginRsp = ${e.message}")
                return null
            }
        }
    }

}

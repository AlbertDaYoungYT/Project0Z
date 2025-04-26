package com.abot.project0z.server.game.packets.recv

import com.abot.project0z.MainActivity
import com.abot.project0z.config.ConfigContainer
import com.abot.project0z.server.game.GameSession
import com.abot.project0z.server.game.packets.PacketHandler
import com.abot.project0z.server.game.packets.net.player.login.PlayerLoginRsp
import com.abot.project0z.utils.Codes

abstract class HandlePlayerLoginRsp : PacketHandler() {


    override fun handle(session: GameSession, header: ByteArray, payload: ByteArray) {
        MainActivity.getLogger().info("Received PlayerLoginReq payload: $payload header: $header")

        val req = PlayerLoginRsp.parse_from(header, payload) ?: return
        if (req.sessionKey == null) {
            MainActivity.getLogger().warn(Codes.ACCOUNT_PARSING_FAILED.details.toLogger())
            return
        }

        MainActivity.config.client.game.session_key = req.sessionKey
    }
}
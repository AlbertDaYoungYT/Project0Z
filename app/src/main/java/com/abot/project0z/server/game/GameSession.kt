package com.abot.project0z.server.game;

import com.abot.project0z.server.GameClient
import com.abot.project0z.server.game.player.Account
import com.abot.project0z.server.game.player.Player


data class GameSession(
    val client: GameClient,
    val sessionKey: String,
    val account: Account?,
    val player: Player?,
    val sessionState: SessionState,
    val connectTime: Long,
    val lastPingTime: Long
) {

    fun duration(): Long = System.currentTimeMillis().minus(connectTime)
}

enum class SessionState {
    INACTIVE,
    WAITING_FOR_TOKEN,
    WAITING_FOR_LOGIN,
    ACTIVE,
    ACCOUNT_BANNED,
}
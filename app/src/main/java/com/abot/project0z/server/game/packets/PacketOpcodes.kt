package com.abot.project0z.server.game.packets


object PacketOpcodes {

    // Empty
    const val NONE = 0

    // Heartbeat & Ping
    const val PingReq = 1
    const val PingRsp = 2

    // Others
    const val QueryPathReq = 3
    const val QueryPathRsp = 4
    const val PlayerTimeNotify = 7
    const val PlayerEventNotify = 8

    // Authentication
    const val PlayerLoginReq = 101
    const val PlayerLoginRsp = 102
    const val PlayerLogoutReq = 103
    const val PlayerLogoutRsp = 104

    // World / Movement
    const val PlayerPositionNotify = 200
    const val WorldObjectSpawnNotify = 201
    const val WorldObjectDespawnNotify = 202
    const val WorldObjectStateUpdateNotify = 203
    const val WorldTimeUpdateNotify = 204
    const val WorldWeatherChangeNotify = 205
    const val WorldEnvironmentSyncReq = 206
    const val WorldEnvironmentSyncRsp = 207
    const val WorldSectorTransferReq = 208
    const val WorldSectorTransferRsp = 209

    const val WorldEventTriggerNotify = 210
    const val WorldEventResultNotify = 211

    const val WorldInteractObjectReq = 212
    const val WorldInteractObjectRsp = 213

    const val WorldNPCSpawnNotify = 220
    const val WorldNPCDespawnNotify = 221
    const val WorldNPCDialogueStartReq = 222
    const val WorldNPCDialogueStartRsp = 223
    const val WorldNPCDialogueOptionReq = 224
    const val WorldNPCDialogueOptionRsp = 225
    const val WorldNPCMoveNotify = 226

    const val WorldItemDropNotify = 230
    const val WorldItemPickupReq = 231
    const val WorldItemPickupRsp = 232

    // Inventory
    const val PlayerInventoryReq = 300
    const val PlayerInventoryRsp = 301
    const val PlayerEquipItemReq = 302
    const val PlayerEquipItemRsp = 303
    const val PlayerUseItemReq = 304
    const val PlayerUseItemRsp = 305

    // Combat
    const val PlayerAttackNotify = 400
    const val PlayerTakeDamageNotify = 401
    const val PlayerDieNotify = 402
    const val EnemySpawnNotify = 403
    const val EnemyDieNotify = 404

    // Abilities
    const val AbilityCastReq = 500
    const val AbilityCastRsp = 501
    const val AbilityResultNotify = 502

    // Chat
    const val ChatSendReq = 600
    const val ChatSendRsp = 601
    const val ChatMessageNotify = 602

    // Sector / World State
    const val SectorEnterReq = 700
    const val SectorEnterRsp = 701
    const val SectorLeaveNotify = 702
    const val SectorStateNotify = 703

    // Shop / Economy
    const val ShopListReq = 800
    const val ShopListRsp = 801
    const val ShopBuyItemReq = 802
    const val ShopBuyItemRsp = 803
    const val CurrencyUpdateNotify = 804

    private val opcodeMap: Map<Int, String> by lazy {
        val map = mutableMapOf<Int, String>()
        val fields = PacketOpcodes::class.java.declaredFields
        for (field in fields) {
            if (field.type == Int::class.javaPrimitiveType) {
                try {
                    val value = field.getInt(null)
                    map[value] = field.name
                } catch (_: Exception) {
                    // Skip if not accessible
                }
            }
        }
        map
    }

    fun get(opcode: Int, default: String = "UNKNOWN"): String {
        return opcodeMap[opcode] ?: default
    }
}
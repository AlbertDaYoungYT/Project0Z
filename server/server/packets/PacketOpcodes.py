

from dataclasses import dataclass

import loguru


class PacketOpcodes:
    # Empty
    NONE: int = 0

    # Heartbeat & Ping
    PingReq = 1
    PingRsp = 2

    # Others
    QueryPathReq = 3
    QueryPathRsp = 4
    PlayerTimeNotify = 7
    PlayerEventNotify = 8

    # Authentication
    PlayerLoginReq = 101
    PlayerLoginRsp = 102
    PlayerLogoutReq = 103
    PlayerLogoutRsp = 104

    # World / Movement (continued)
    PlayerPositionNotify = 200
    WorldObjectSpawnNotify = 201
    WorldObjectDespawnNotify = 202
    WorldObjectStateUpdateNotify = 203
    WorldTimeUpdateNotify = 204
    WorldWeatherChangeNotify = 205
    WorldEnvironmentSyncReq = 206
    WorldEnvironmentSyncRsp = 207
    WorldSectorTransferReq = 208
    WorldSectorTransferRsp = 209

    WorldEventTriggerNotify = 210
    WorldEventResultNotify = 211

    WorldInteractObjectReq = 212
    WorldInteractObjectRsp = 213

    WorldNPCSpawnNotify = 220
    WorldNPCDespawnNotify = 221
    WorldNPCDialogueStartReq = 222
    WorldNPCDialogueStartRsp = 223
    WorldNPCDialogueOptionReq = 224
    WorldNPCDialogueOptionRsp = 225
    WorldNPCMoveNotify = 226

    WorldItemDropNotify = 230
    WorldItemPickupReq = 231
    WorldItemPickupRsp = 232

    # Inventory
    PlayerInventoryReq = 300
    PlayerInventoryRsp = 301
    PlayerEquipItemReq = 302
    PlayerEquipItemRsp = 303
    PlayerUseItemReq = 304
    PlayerUseItemRsp = 305

    # Combat
    PlayerAttackNotify = 400
    PlayerTakeDamageNotify = 401
    PlayerDieNotify = 402
    EnemySpawnNotify = 403
    EnemyDieNotify = 404

    # Abilities
    AbilityCastReq = 500
    AbilityCastRsp = 501
    AbilityResultNotify = 502

    # Chat
    ChatSendReq = 600
    ChatSendRsp = 601
    ChatMessageNotify = 602

    # Sector / World State
    SectorEnterReq = 700
    SectorEnterRsp = 701
    SectorLeaveNotify = 702
    SectorStateNotify = 703

    # Shop / Economy
    ShopListReq = 800
    ShopListRsp = 801
    ShopBuyItemReq = 802
    ShopBuyItemRsp = 803
    CurrencyUpdateNotify = 804


    _opcode_map = {}

    @classmethod
    def _initialize_opcode_map(cls):
        if not cls._opcode_map:
            for name in dir(cls):
                if not name.startswith("__") and isinstance(getattr(cls, name), int):
                    cls._opcode_map[getattr(cls, name)] = name

    @classmethod
    def get(cls, opcode: int, default: str = "UNKNOWN") -> str:
        cls._initialize_opcode_map()
        return cls._opcode_map.get(opcode, default)

    @classmethod
    def dump_packet_ids(cls, filename_prefix: str = "PacketIds", version: str = "1.0"):
        cls._initialize_opcode_map()
        sorted_packets = dict(sorted(cls._opcode_map.items()))
        import json
        filename = f"./{filename_prefix}_{version}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(sorted_packets, f, indent=4)
            loguru.logger.info(f"Dumped packet IDs to {filename}")
        except IOError as e:
            loguru.logger.error(f"Error dumping packet IDs: {e}")
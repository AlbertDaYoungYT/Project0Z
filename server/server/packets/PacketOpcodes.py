from dataclasses import dataclass

import loguru


class PacketOpcodes:
    NONE: int = 0

    # Heartbeat & Ping
    PING_REQUEST: int = 1
    PING_RESPONSE: int = 2

    # Authentication
    CLIENT_XOR_KEY_REQUEST: int = 98
    CLIENT_XOR_KEY_SUBMISSION: int = 99

    # Player Management
    PLAYER_LOGIN_REQUEST: int = 101
    PLAYER_LOGIN_RESPONSE: int = 102
    PLAYER_LOGOUT_REQUEST: int = 103
    PLAYER_LOGOUT_RESPONSE: int = 104

    PLAYER_TIME_NOTIFY: int = 105
    PLAYER_EVENT_NOTIFY: int = 106

    # World / Movement Management
    PLAYER_POSITION_UPDATE_NOTIFY: int = 200
    WORLD_OBJECT_SPAWN_NOTIFY: int = 201
    WORLD_OBJECT_DESPAWN_NOTIFY: int = 202
    WORLD_OBJECT_STATE_UPDATE_NOTIFY: int = 203
    WORLD_TIME_UPDATE_NOTIFY: int = 204
    WORLD_WEATHER_CHANGE_NOTIFY: int = 205
    WORLD_ENVIRONMENT_SYNC_REQUEST: int = 206
    WORLD_ENVIRONMENT_SYNC_RESPONSE: int = 207
    WORLD_SECTOR_TRANSFER_REQUEST: int = 208
    WORLD_SECTOR_TRANSFER_RESPONSE: int = 209

    WORLD_EVENT_TRIGGER_NOTIFY: int = 210
    WORLD_EVENT_RESULT_NOTIFY: int = 211

    WORLD_INTERACT_OBJECT_REQUEST: int = 212
    WORLD_INTERACT_OBJECT_RESPONSE: int = 213

    WORLD_NPC_SPAWN_NOTIFY: int = 220
    WORLD_NPC_DESPAWN_NOTIFY: int = 221
    WORLD_NPC_DIALOGUE_START_REQUEST: int = 222
    WORLD_NPC_DIALOGUE_START_RESPONSE: int = 223
    WORLD_NPC_DIALOGUE_OPTION_REQUEST: int = 224
    WORLD_NPC_DIALOGUE_OPTION_RESPONSE: int = 225
    WORLD_NPC_MOVE_NOTIFY: int = 226

    WORLD_ITEM_DROP_NOTIFY: int = 230
    WORLD_ITEM_PICKUP_REQUEST: int = 231
    WORLD_ITEM_PICKUP_RESPONSE: int = 232

    # Inventory Management
    PLAYER_INVENTORY_REQUEST: int = 300
    PLAYER_INVENTORY_RESPONSE: int = 301
    PLAYER_EQUIP_ITEM_REQUEST: int = 302
    PLAYER_EQUIP_ITEM_RESPONSE: int = 303
    PLAYER_USE_ITEM_REQUEST: int = 304
    PLAYER_USE_ITEM_RESPONSE: int = 305

    # Combat Management
    PLAYER_ATTACK_NOTIFY: int = 400
    PLAYER_TAKE_DAMAGE_NOTIFY: int = 401
    PLAYER_DIE_NOTIFY: int = 402
    ENEMY_SPAWN_NOTIFY: int = 403
    ENEMY_DIE_NOTIFY: int = 404

    # Abilities Management
    ABILITY_CAST_REQUEST: int = 500
    ABILITY_CAST_RESPONSE: int = 501
    ABILITY_RESULT_NOTIFY: int = 502

    # Chat Management
    CHAT_SEND_REQUEST: int = 600
    CHAT_SEND_RESPONSE: int = 601
    CHAT_MESSAGE_NOTIFY: int = 602

    # Sector / World State Management
    SECTOR_ENTER_REQUEST: int = 700
    SECTOR_ENTER_RESPONSE: int = 701
    SECTOR_LEAVE_NOTIFY: int = 702
    SECTOR_STATE_NOTIFY: int = 703

    # Shop / Economy Management
    SHOP_LIST_REQUEST: int = 800
    SHOP_LIST_RESPONSE: int = 801
    SHOP_BUY_ITEM_REQUEST: int = 802
    SHOP_BUY_ITEM_RESPONSE: int = 803
    CURRENCY_UPDATE_NOTIFY: int = 804

    _opcode_map: dict[int, str] = {}

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
    def dump_to_file(cls, filename: str):
        with open(filename, 'w') as file:
            for value in sorted(cls._opcode_map.keys()):
                name = cls._opcode_map[value]
                file.write(f"{value}: {name}\n")
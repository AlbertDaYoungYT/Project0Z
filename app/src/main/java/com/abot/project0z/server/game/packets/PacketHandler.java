package com.abot.project0z.server.game.packets;

import com.abot.project0z.server.game.GameSession;

public abstract class PacketHandler {
    protected static final byte[] EMPTY_BYTE_ARRAY = new byte[0];

    public abstract void handle(GameSession session, byte[] header, byte[] payload) throws Exception;
}

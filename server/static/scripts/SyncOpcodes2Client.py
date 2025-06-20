
from config.ConfigContainer import ConfigContainer
from server.packets.BasePacket import BasePacket
from server.GameSession import GameSession
from utils.AppServices import AppServices


def execute(config: ConfigContainer, services: AppServices, session: GameSession) -> BasePacket:
    packet = None

    return packet
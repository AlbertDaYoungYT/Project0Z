import importlib
import inspect
import pkgutil
from typing import Dict, Type

import loguru
from server.GameSession import GameSession, SessionState
from server.packets.PacketHandler import PacketHandler
from server.packets.PacketOpcodes import PacketOpcodes
from utils.AppServices import AppServices


class GameServerPacketHandler:
    def __init__(self, handler_base_class: Type[PacketHandler], services: AppServices):
        self.handlers: Dict[int, PacketHandler] = {}
        self.services = services
        self.register_handlers(handler_base_class)


    def register_packet_handler(self, handler_class: Type[PacketHandler]):
        opcode_decorator = getattr(handler_class, 'opcode', None)
        disabled = getattr(handler_class, 'disabled', False)

        if opcode_decorator is not None and not disabled and opcode_decorator > 0:
            try:
                packet_handler = handler_class()
                self.handlers[opcode_decorator] = packet_handler
                loguru.logger.debug(f"Registered handler {handler_class.__name__} for opcode {opcode_decorator}")
            except Exception as e:
                loguru.logger.warning(f"Unable to register handler {handler_class.__name__}: {e}")

    def register_handlers(self, handler_base_class: Type[PacketHandler]):
        handler_package = "server.packets.recv"  # The name of your package containing handlers

        try:
            module = importlib.import_module(handler_package)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, handler_base_class) and obj != handler_base_class:
                    self.register_packet_handler(obj)

            # Recursively scan submodules if needed
            for _, module_name, is_pkg in pkgutil.walk_packages(module.__path__, prefix=module.__name__ + "."):
                if not is_pkg:
                    try:
                        sub_module = importlib.import_module(module_name)
                        for name, obj in inspect.getmembers(sub_module):
                            if inspect.isclass(obj) and issubclass(obj, handler_base_class) and obj != handler_base_class:
                                self.register_packet_handler(obj)
                    except ImportError as e:
                        loguru.logger.warning(f"Error importing submodule {module_name}: {e}")

        except ImportError as e:
            loguru.logger.error(f"Could not import packet handler package '{handler_package}': {e}")

        loguru.logger.debug(f"Registered {len(self.handlers)} {handler_base_class.__name__}s")


    async def handle(self, session: GameSession, opcode: int, header: bytes, payload: bytes):
        handler = self.handlers.get(opcode)

        if handler:
            try:
                state = session.state

                # Session state checks (similar to Java)
                if opcode == PacketOpcodes.PingReq:
                    pass  # Always continue for PingReq
                #elif opcode == PacketOpcodes.GetPlayerTokenReq:
                #    if state != SessionState.WAITING_FOR_TOKEN:
                #        return
                elif state == SessionState.ACCOUNT_BANNED:
                    await session.close()
                    return
                elif opcode == PacketOpcodes.PlayerLoginReq:
                    if state != SessionState.WAITING_FOR_LOGIN:
                        return
                #elif opcode == PacketOpcodes.SetPlayerBornDataReq:
                #    if state != SessionState.PICKING_CHARACTER:
                #        return
                else:
                    if state != SessionState.ACTIVE:
                        return

                # Placeholder for event system (you'd need to implement this)
                # event = ReceivePacketEvent(session, opcode, payload)
                # event.call()
                # if not event.is_canceled():
                await handler.handle(session, header, payload)

            except Exception as ex:
                loguru.logger.exception(f"Error handling packet with opcode {opcode}:")

            return  # Packet successfully handled

        # Log unhandled packets
        loguru.logger.info(f"Unhandled packet (opcode {opcode}): {PacketOpcodes.get(opcode, 'Unknown')}")



from uuid import UUID
import loguru
from server.GameSession import GameSession, SessionState
from server.packets.PacketHandler import PacketHandler
from server.packets.PacketOpcodes import PacketOpcodes
from server.packets.Opcodes import opcodes
from server.packets.net.player.login.PlayerLoginReq import PlayerLoginReq
from server.packets.send.PacketPlayerLoginRsp import PacketPlayerLoginRsp
from server.player.Account import Account
from server.player.Player import Player
from utils.Errors import Codes


@opcodes(value=PacketOpcodes.PLAYER_LOGIN_REQUEST)
class HandlerPlayerLoginReq(PacketHandler):
    async def handle(self, session: GameSession, header: bytes, payload: bytes):
        loguru.logger.info(f"Received PlayerLoginReq payload: {payload} header: {header}")

        # Parse request
        req = PlayerLoginReq.parse_from(payload)
        if req is None:
            loguru.logger.debug(Codes.ACCOUNT_CHECK_FAILED.to_logger())
            await session.close()
            return
        

        # Check
        if session.get_account() is None:
            try:
                account = await session.services.account_repository.get_account_by_token(req.token)
                session.set_account(account)
            except Exception as e:
                loguru.logger.debug(Codes.ACCOUNT_CHECK_FAILED.to_logger())
                await session.close()
                return 


        # Authenticate session
        if session.get_account().token != req.token: # Assuming Account object has a 'token' attribute
            loguru.logger.debug(Codes.ACCOUNT_NOT_VERIFIED.to_logger())
            await session.close()
            return

        # Load character from db (placeholder)
        player = session.get_player()
        if player is None:
            player = await session.services.player_repository.get_player_by_account_id(account.account_id)
            if player is None:
                player = Player(
                    id=None,
                    account=session.get_account(),
                    account_id=None,
                    session=session,
                    session_key=None
                )
                await session.services.player_repository.create_player(player)
            session.set_player(player)
        player.on_login()

        # Final packet to tell client logging in is done
        await session.send(PacketPlayerLoginRsp(session))
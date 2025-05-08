
from dataclasses import dataclass
import secrets
from uuid import UUID
import loguru


from server.player.Account import Account
from server.states.SessionState import SessionState
from utils.DatabaseAdapter import Serializable
from utils.Vectors import Vector2d


@dataclass
class Player:
    id: UUID
    session: object

    account: Account
    account_id: UUID
    username: str

    position: Vector2d


    has_sent_login_packets: bool

    def __init__(self):
        self.id = None
        self.session: object = None

        self.has_sent_login_packets = False

        if self.id == None:
            self.id = UUID(secrets.token_hex(16))




    def on_login(self):
        loguru.logger.info("Player logged in.")
        
        self.has_sent_login_packets = True
        self.session.state = SessionState.ACTIVE

    def on_logout(self):
        try:
            # Save to db
            self.save()
        except Exception as e:
            loguru.logger.warn(f"Player (UID {self.id}) save failure")
        finally:
            self.remove_from_server()
    
    def remove_from_server(self):
        loguru.logger.info(f"Player (UID {self.id}) removed from server")
        self.session.close()
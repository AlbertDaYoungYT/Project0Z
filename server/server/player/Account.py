

from dataclasses import dataclass
from uuid import UUID
import uuid
from utils.DatabaseAdapter import Serializable
from utils.types.Locale import Locale

import secrets
import hashlib
import time


def generate_account_token(user_id: str) -> str:
    """
    Generates a secure login token for a given user.
    
    Args:
        user_id (str): The user's unique ID (not the token).
        
    Returns:
        str: A secure, unique login token.
    """
    # Combine user ID, current time, and a secure random value
    raw_data = f"{user_id}:{time.time()}:{secrets.token_hex(16)}"
    
    # Hash the combined data for fixed length and security
    token = hashlib.sha256(raw_data.encode()).hexdigest()
    
    return token

@dataclass
class Account:
    account_id: UUID
    username: str
    password: str
    email: str

    token: str

    bank_balance: float
    bank_currency: float
    bank_silver: float
    bank_gold: float

    session_key: str


    locale: Locale
    ban_reason: str
    ban_end_time: float
    ban_start_time: float
    is_banned: bool

    def __init__(self):
        self.account_id = None
        self.username = ""
        self.password = ""
        self.email = ""

        self.token = None

        self.session_key: str = "" # hashlib.sha256(UUID(secrets.token_hex(16)).bytes).hexdigest()
        
        self.locale: Locale = Locale.ENGLISH
        self.ban_reason: str = ""
        self.ban_end_time: float = 0.0
        self.ban_start_time: float = 0.0
        self.is_banned: bool = False

        if self.account_id == None:
            self.account_id = UUID(secrets.token_hex(16))

        if self.token == None:
            self.token = generate_account_token(self.account_id.hex)


    def create_session_key(self):
        self.session_key = hashlib.sha256(UUID(secrets.token_hex(16)).bytes).hexdigest()
        return self.session_key

    def load(self):
        pass


    def save(self):
        pass


    def has_permission(permission_node: str) -> bool:
        pass

    def to_client(self) -> dict:
        if self.is_banned:
            return {
                "account_id": self.account_id,
                "username": self.username,
                "is_banned": self.is_banned,
                "ban_end_time": self.ban_end_time,
                "ban_reason": self.ban_reason
            }
        else:
            return {
                "account_id": self.account_id,
                "username": self.username,
                "token": self.token
            }
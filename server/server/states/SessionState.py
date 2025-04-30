
from enum import Enum


class SessionState(Enum):
    INACTIVE = "INACTIVE"
    WAITING_FOR_TOKEN = "WAITING_FOR_TOKEN"
    WAITING_FOR_LOGIN = "WAITING_FOR_LOGIN"
    ACTIVE = "ACTIVE"
    ACCOUNT_BANNED = "ACCOUNT_BANNED"
    # Add other states as needed
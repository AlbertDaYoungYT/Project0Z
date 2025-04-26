from dataclasses import dataclass
from uuid import UUID

from . import Model
from permissions.PermissionManager import Permission
from utils.Locale import Locale


@dataclass
class AccountModel(Model):
    account_id: UUID
    username: str
    password: str
    email: str

    token: str

    bank_balance: float
    bank_currency: float
    bank_silver: float
    bank_gold: float

    permissions: list[Permission]
    locale: Locale
    ban_reason: str
    ban_end_time: float
    ban_start_time: float
    is_banned: bool
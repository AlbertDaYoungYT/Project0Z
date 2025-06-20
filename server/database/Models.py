
from dataclasses import dataclass
from enum import Enum
import inspect
from uuid import UUID
import secrets
from datetime import date, datetime, timedelta

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import Certificate
from utils.types.Locale import Locale
from utils.types.Vectors import Vector2d
from utils.DatabaseAdapter import Serializable

class Modelable:
    
    @classmethod
    def __set__(cls, **kwargs):
        for k,v in kwargs.items():
            cls.__setattr__(k,v)
        
        return cls


@dataclass
class Model(Serializable):


    @classmethod
    def from_class(cls, other) -> Serializable:
        self_attributes = inspect.getmembers(cls, lambda a:not(inspect.isroutine(a)))
        other_attributes = inspect.getmembers(other, lambda a:not(inspect.isroutine(a)))

        list_of_self_attr = [a for a in self_attributes if not(a[0].startswith('__') and a[0].endswith('__'))]

        for k,v in [a for a in other_attributes if not(a[0].startswith('__') and a[0].endswith('__'))]:
            if (k, v) in list_of_self_attr:
                cls.__setattr__(k, v)
        
        return cls

    @classmethod
    def to_class(cls, clazz: Modelable) -> Modelable:
        self_attributes = dict(inspect.getmembers(cls, lambda a:not(inspect.isroutine(a))))
        return clazz.__set__(self_attributes)

class DataStores(Enum):
    DEFAULT: int = 1
    HTTP_AUTH_FLOW: int = 2

    AUTHENTICATION: int = 10
    ACCOUNT: int = 11
    CERTIFICATE: int = 12
    CRASH_REPORT: int = 13
    PLAYER: int = 14
    CHATS: int = 15




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

    locale: Locale
    ban_reason: str
    ban_end_time: float
    ban_start_time: float
    is_banned: bool


@dataclass
class CertificateModel(Model):
    certificate_id: UUID = UUID(secrets.token_hex(16))
    auth_id: str | None = None
    account_id: UUID | None = None

    expire_timestamp: float = datetime.timestamp(datetime.now() + timedelta(7))

    certificate: Certificate | None = None
    private_key: rsa.RSAPrivateKey | None = None
    public_key: rsa.RSAPublicKey | None = None

    original_challenge: str | None = None
    encrypted_challenge: str | None = None
    xor_key: str | None = None


@dataclass
class CrashReportModel(Model):
    report_id: UUID
    account_id: UUID
    email: str
    token: str

    crash_report: list[dict]
    logcat_report: list[dict]


@dataclass
class PlayerModel(Model):
    id: UUID
    account_id: UUID
    player_ship_id: UUID
    session_key: str

    player_location: Vector2d

@dataclass
class PlayerChatModel(Model):
    message_id: UUID
    
    sender_id: UUID
    reciever_id: UUID

    message: str
    timestamp: float


@dataclass
class Position(Model):
    """
    A dataclass representing a 3D position.  It uses a custom JSON adapter
    to handle serialization/deserialization.
    """
    x: float
    y: float
    z: float = 0.0  # Default value for z
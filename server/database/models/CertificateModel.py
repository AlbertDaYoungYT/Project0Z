from dataclasses import dataclass
import secrets
from uuid import UUID
from datetime import date, datetime, timedelta

from . import Model
from cryptography.hazmat.primitives.asymmetric import rsa
from permissions.PermissionManager import Permission
from cryptography.x509 import Certificate
from utils.Locale import Locale


@dataclass
class CertificateModel(Model):
    certificate_id: UUID = UUID(secrets.token_hex(16))
    auth_id: str | None = None
    account_id: UUID | None = None

    expire_timestamp: float = datetime.timestamp(datetime.now() + timedelta(7))

    certificate: Certificate | None = None
    private_key: rsa.RSAPrivateKey | None = None
    public_key: rsa.RSAPublicKey | None = None
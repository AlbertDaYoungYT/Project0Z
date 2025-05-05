
from dataclasses import dataclass
from uuid import UUID

from database.models.CertificateModel import CertificateModel

from . import DataStore


@dataclass
class CertificateDataStore(DataStore):
    client_id: UUID
    new_client_id: UUID | None = None

    auth_id: str
    
    session_cert_model: CertificateModel
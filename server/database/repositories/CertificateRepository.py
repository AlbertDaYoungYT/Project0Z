
from uuid import UUID
from datetime import date, datetime, timedelta
import loguru

from config.ConfigContainer import ConfigContainer
from database.DatabaseManager import CouchDBManager
from database.Models import *
from server.player.Account import Account

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import Certificate

class CertificateRepository(CouchDBManager):

    def __init__(self, server: CouchDBManager, server_url: str, config: ConfigContainer):
        self.DATABASE_NAME = config.couchdb_collection + "_certificates"
        self.server_url = server_url
        self.config = config
        self.server = server

        self._link_to_cache(db=DataStores.CERTIFICATE)
        loguru.logger.debug(f"Initiated CouchDB Repo: {self.DATABASE_NAME}")

    async def create_certificate(self,
                                 id: UUID,
                                 auth_id: str,
                                 certificate: Certificate,
                                 private_key: rsa.RSAPrivateKey,
                                 public_key: rsa.RSAPublicKey | None = None
                                 )\
            -> CertificateModel | None:
        """Create a new certificate."""
        cert_model = CertificateModel(
            certificate_id=id,
            auth_id=auth_id,
            expire_timestamp=datetime.timestamp(datetime.now() + timedelta(7)),
            certificate=certificate,
            private_key=private_key,
            public_key=public_key
        )
        result = await self.server.save_document(self.DATABASE_NAME, cert_model)
        if result:
            cert_model.certificate_id = result[0]  # Update certificate ID with the CouchDB ID
            return cert_model
        return None

    async def get_certificate_by_id(self, id: str) -> CertificateModel | None:
        """Get an certificate by its ID."""
        doc = await self.server.get_document(self.DATABASE_NAME, id)
        if doc:
            return CertificateModel.from_dict(doc)
        return None

    async def get_certificate_by_account_id(self, account_id: UUID) -> CertificateModel | None:
        """Get an certificate by its account id."""
        query = {"selector": {"account_id": account_id}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return CertificateModel.from_dict(results[0])
        return None

    async def get_certificate_by_auth_token(self, auth_token: str) -> CertificateModel | None:
        """Get an certificate by its account id."""
        query = {"selector": {"auth_id": auth_token}}
        results = await self.server.find_documents(self.DATABASE_NAME, query)
        if results:
            return CertificateModel.from_dict(results[0])
        return None

    async def update_certificate(self, certificate: CertificateModel) -> CertificateModel | None:
        """Update an existing certificate."""
        doc = certificate.to_dict()
        existing_doc = await self.server.get_document(self.DATABASE_NAME, certificate.certificate_id)
        if existing_doc:
            doc["_rev"] = existing_doc["_rev"]  # Include the revision for updating
            result = await self.server.save_document(self.DATABASE_NAME, doc)
            return result is not None
        return False

    async def assign_account_id_to_certificate(self, certificate: CertificateModel, account_id: UUID) -> CertificateModel | None:
        """Update an existing certificate."""
        certificate.account_id = account_id
        doc = certificate.to_dict()
        existing_doc = await self.get_document(self.DATABASE_NAME, certificate.certificate_id)
        if existing_doc:
            doc["_rev"] = existing_doc["_rev"]  # Include the revision for updating
            result = await self.server.save_document(self.DATABASE_NAME, doc)
            return result is not None
        return False

    async def delete_certificate(self, certificate_id: str):
        """Delete an certificate by its ID."""
        return await self.server.delete_document(self.DATABASE_NAME, certificate_id)

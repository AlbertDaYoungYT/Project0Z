import base64
import json, loguru, hashlib, secrets
from uuid import UUID
import time
from aiohttp import web
from database.Models import *
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
from cryptography.hazmat.backends import default_backend

async def challenge_submission_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return Codes.INVALID_FIELD_VALUE.to_response()
    if _json.get("challenge_submission") == None: return Codes.INVALID_FIELD_VALUE.to_response()
    id = _json.get("id")
    client_submitted_challenge = _json.get("challenge_submission")

    loguru.logger.debug(f"Signing Challenge Submission from {request.remote}")

    # The Client Auth and Key data is fetched from the previous step
    stored_client_auth: CertificateModel | None = await services.redisdb.get(f"CLIENT::CHALLENGE::{request.remote}::{id}", CertificateModel)
    if stored_client_auth == None: return Codes.CLIENT_INVALID_ID.to_response()

    # Clients signed challenge is decrypted and verify it against the servers
    loaded_client_public_key = load_pem_public_key(
        base64.b64decode(stored_client_auth.public_key[len("BASE64::CLIENT_PUBLIC_KEY::"):].encode()),
        backend=default_backend()
    )
    try:
        res = loaded_client_public_key.verify(
            base64.b64decode(client_submitted_challenge[len("BASE64::CHALLENGE::"):].encode()),
            base64.b64decode(stored_client_auth.original_challenge[len("SHA256::CHALLENGE::"):].encode()),
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hashes.SHA256()
        )
    except Exception as e:
        loguru.logger.error(Codes.CLIENT_CHALLENGE_VERIFICATION_FAILED.to_logger(e))
        return Codes.CLIENT_CHALLENGE_VERIFICATION_FAILED.to_response()
    finally:
        # Delete any left over Redis Entries from the Authentication Process
        await services.redisdb.delete(f"CLIENT::CHALLENGE::{request.remote}::{id}")


    # Generate Client Auth ID from Client ID
    auth_id = hashlib.md5(id.encode()).hexdigest()
    session_cert = services.session_key_manager.generate_session_cert(UUID(auth_id))
    session_private_key = services.session_key_manager.get_signed_cert_full(UUID(auth_id))[0]
    certificate_model = await services.certificate_repository.create_certificate(
        id=UUID(id),
        auth_id=auth_id,
        certificate=session_cert,
        private_key=session_private_key
    )
    if certificate_model == None: return Codes.DATABASE_QUERY_ERROR.to_response()

    await services.redisdb.add(f"CLIENT::CERTIFICATE::{request.remote}::{id}", CertificateModel.from_dict({
        "id": id,
        "auth_id": auth_id,
        "certificate": certificate_model.certificate
    }))

    return web.json_response({
        "id": id,
        "auth_id": auth_id,
        "session_certificate": "BASE64::CERTIFICATE::"+base64.b64encode(session_cert.public_bytes(
                                    Encoding.PEM
                                )).decode()
    })
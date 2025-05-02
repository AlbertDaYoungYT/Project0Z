import base64
import json, loguru, hashlib, secrets
from uuid import UUID
import time
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

async def signing_challenge_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return Codes.INVALID_FIELD_VALUE.to_response()
    id = _json.get("id")

    loguru.logger.debug(f"Signing Challenge Request from {request.remote}")

    # Get Clients Public Key from Redis
    client_public_key = json.loads(services.redis_server.get_redis().get(f"BASE64::CLIENT_PUBLIC_KEY::{id}"))
    if client_public_key == None: return Codes.CLIENT_INVALID_ID.to_response()
    client_public_key = client_public_key["client_public_key"]

    loaded_client_public_key = load_pem_public_key(
        base64.b64decode(client_public_key[len("BASE64::CLIENT_PUBLIC_KEY::"):].encode())
    )

    # Challenge is generated, encrypted and signed
    try:
        original_challenge = hashlib.sha256(secrets.token_bytes(256))
        challenge = loaded_client_public_key.encrypt(
            original_challenge.digest(),
            padding=padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        original_challenge = base64.b64encode(original_challenge.digest()).decode()
        challenge = base64.b64encode(challenge).decode()
    except Exception as e:
        loguru.logger.error(Codes.FAILED_GENERATING_AUTH_CHALLENGE.to_logger(e))
        return Codes.FAILED_GENERATING_AUTH_CHALLENGE.to_response()

    # Generate new UUID for client
    new_id = UUID(secrets.token_hex(16)).hex
    services.redis_server.get_redis().delete(f"BASE64::CLIENT_PUBLIC_KEY::{id}")

    res = {
        "id": new_id,
        "encrypted_challenge": f"BASE64::CHALLENGE::{challenge}"
    }
    
    try:
        services.redis_server.get_redis().set(f"CLIENT::CHALLENGE::{request.remote}::{new_id}", json.dumps({
            "id": new_id,
            "client_public_key": client_public_key,
            "original_challenge": f"SHA256::CHALLENGE::{original_challenge}",
            "encrypted_challenge": f"BASE64::CHALLENGE::{challenge}",
            "_timestamp": time.time()
        }))
    except Exception as e:
        loguru.logger.error(Codes.DATABASE_QUERY_ERROR.to_logger(e))
        return Codes.DATABASE_QUERY_ERROR.to_response()

    return web.json_response(res)
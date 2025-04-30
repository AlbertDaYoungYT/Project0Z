import json, loguru, hashlib, secrets
from uuid import UUID
import time
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def challenge_submission_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return web.json_response(Codes.INVALID_FIELD_VALUE.value.to_dict())
    if _json.get("challenge") == None: return web.json_response(Codes.INVALID_FIELD_VALUE.value.to_dict())
    id = _json.get("id")
    signed_challenge = _json.get("challenge")

    loguru.logger.debug(f"Signing Challenge Submission from {request.remote}")

    original_challenge = services.redis_server.get_redis().get(f"CHALLENGE_{id}")["challenge"]
    signed_original_challenge = services.ca_authority.root_private_key.sign(original_challenge.encode()).decode()

    if signed_challenge != signed_original_challenge: return web.json_response(Codes.CLIENT_CHALLENGE_VERIFICATION_FAILED.value.to_dict())

    auth_token = hashlib.md5(secrets.token_bytes(64)).hexdigest()
    session_key = services.session_key_manager.generate_session_cert(UUID(id)).public_key().public_bytes_raw()

    services.redis_server.get_redis().set(f"SESSION_KEY_{id}", {
        "id": id,
        "auth_token": auth_token,
        "session_key": session_key.decode(),
        "_timestamp": time.time()
    })

    return web.json_response({
        "id": id,
        "auth_token": auth_token,
        "session_key": session_key.decode()
    })
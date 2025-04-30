import json, loguru, hashlib, secrets
import time
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def signing_challenge_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return web.json_response(Codes.INVALID_FIELD_VALUE.value.to_dict())
    id = _json.get("id")

    loguru.logger.debug(f"Signing Challenge Request from {request.remote}")

    challenge = hashlib.sha256(secrets.token_bytes(256)).hexdigest()
    res = {
        "id": id,
        "challenge": challenge
    }
    
    services.redis_server.get_redis().set(f"CHALLENGE_{id}", {
        "id": id,
        "challenge": challenge,
        "_timestamp": time.time()
    })

    return web.json_response(res)
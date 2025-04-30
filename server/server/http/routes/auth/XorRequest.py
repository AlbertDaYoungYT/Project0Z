import json, loguru, hashlib, secrets
import time
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def xor_key_create_request_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return web.json_response(Codes.INVALID_FIELD_VALUE.value.to_dict())
    id = _json.get("id")

    loguru.logger.debug(f"XOR Key Creation Request from {request.remote}")

    xor_key = hashlib.md5(secrets.token_bytes(32)).hexdigest()
    services.redis_server.get_redis().set(f"XOR_{id}", {
        "id": id,
        "xor_key": xor_key,
        "_timestamp": time.time()
    })

    return web.json_response({
        "id": id,
        "xor_key": xor_key
    })

async def xor_key_get_request_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return web.json_response(Codes.INVALID_FIELD_VALUE.value.to_dict())
    id = _json.get("id")

    loguru.logger.debug(f"XOR Key Fetch Request from {request.remote}")
    
    return web.json_response(services.redis_server.get_redis().get(f"XOR_{id}"))
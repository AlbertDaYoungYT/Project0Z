import json, loguru
import time
import secrets, base64
from uuid import UUID
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

async def initial_ack_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return web.json_response(Codes.INVALID_FIELD_VALUE.to_dict())
    if _json.get("client_public_key") == None: return web.json_response(Codes.INVALID_FIELD_VALUE.to_dict())
    id = _json.get("id")
    client_public_key = _json.get("client_public_key")

    loguru.logger.debug(f"Initial ACK Response from {request.remote}")


    server_public_key = services.ca_authority.root_private_key.public_key().public_bytes(
        Encoding.PEM,
        PublicFormat.SubjectPublicKeyInfo
    )
    server_public_key = "BASE64::SERVER_PUBLIC_KEY::"+base64.b64encode(server_public_key).decode()

    # Generate new UUID to client
    id = UUID(secrets.token_hex(16)).hex
    res = {
        "id": id,
        "server_public_key": server_public_key
    }
    
    services.redis_server.get_redis().set(f"BASE64::CLIENT_PUBLIC_KEY::{id}", json.dumps({
        "id": id,
        "client_public_key": client_public_key,
        "_timestamp": time.time()
    }))

    return web.json_response(res)
import json, loguru
import secrets, base64
from uuid import UUID
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def initial_ack_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    loguru.logger.debug(f"Initial ACK Response from {request.remote}")
    id = _json.get("id", None)
    if id == None: return web.json_response(Codes.ITEM_NOT_FOUND.value.to_dict())
    loguru.logger.debug(services.ca_authority.root_private_key.public_key().public_bytes("Raw", "Raw"))
    res = {
        "id": id,
        "public_key": base64.urlsafe_b64encode(services.ca_authority.root_private_key.public_key().public_bytes("Raw", "Raw")).decode()
    }

    return web.json_response(res)
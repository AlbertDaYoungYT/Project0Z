import json, loguru
import secrets, base64
from uuid import UUID
from aiohttp import web
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def initial_ack_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    loguru.logger.debug(f"Initial ACK Request from {request.remote}")
    id = _json.get("id", UUID(secrets.token_bytes(16)))
    
    res = {
        "id": id,
        "session_key": base64.urlsafe_b64encode(services.session_key_manager.generate_session_cert(id).tbs_certificate_bytes).decode()
    }

    return web.json_response(res)
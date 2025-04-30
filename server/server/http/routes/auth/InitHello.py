import json, loguru
from uuid import UUID
import secrets
import time
from aiohttp import web
import requests
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def initial_greeting_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())
    
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    region = {
        "SHORT": f"{data.get('timezone').split('/')[0].capitalize()}-{data.get('country')}",
        "COUNTRY": f"{data.get('country')}-{data.get('region').lower().replace(' ', '_')}"
    }

    loguru.logger.debug(f"Greeting Request from {request.remote}")

    # Check if Client version is supported by server
    if sum(services.game_constants.MIN_CLIENT_VERSION) > sum(_json["client_version"]):
        return web.json_response(Codes.CLIENT_VERSION_TOO_LOW.value.to_dict())
    
    res = {
        "id": UUID(secrets.token_bytes(16)).hex,
        "version": services.game_constants.VERSION,
        "min_client_version": services.game_constants.MIN_CLIENT_VERSION,
        "region": region["SHORT"],
        "uptime": time.strftime("%-Hh %-Mm %-Ss", time.gmtime(time.time()-services.uptime))
    }

    return web.json_response(res)
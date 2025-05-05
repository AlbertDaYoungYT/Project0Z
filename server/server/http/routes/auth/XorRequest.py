import json, loguru, hashlib, secrets
import time
from aiohttp import web
from database.models.CertificateModel import CertificateModel
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

# TODO: Temporary XOR Implementation
async def xor_key_create_request_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return Codes.INVALID_FIELD_VALUE.to_response()
    id = _json.get("id")

    loguru.logger.debug(f"XOR Key Creation Request from {request.remote}")

    xor_key = hashlib.md5(secrets.token_bytes(32)).hexdigest()
    await services.redisdb.add(f"CLIENT::XOR::{request.remote}::{id}", CertificateModel.from_dict({
        "id": id,
        "xor_key": xor_key
    }))

    return web.json_response({
        "id": id,
        "xor_key": xor_key
    })

async def xor_key_get_request_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("id") == None: return Codes.INVALID_FIELD_VALUE.to_response()
    id = _json.get("id")

    loguru.logger.debug(f"XOR Key Fetch Request from {request.remote}")
    
    return web.json_response((await services.redisdb.get(f"CLIENT::XOR::{request.remote}::{id}")).to_json())
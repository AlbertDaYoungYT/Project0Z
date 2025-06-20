import hashlib
import json, loguru
from uuid import UUID
import secrets
import time
from aiohttp import web
import requests
from database.Models import *
from utils.AppServices import AppServices
from utils.types.Errors import Codes  # Import the Router instance (see step 3)

async def initial_greeting_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())
    if "auth_token" in _json.keys()\
            and\
            "id"    in _json.keys():
        return await returning_greeting_handler(request, services)
    
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    region = {
        "SHORT": f"{data.get('timezone').split('/')[0].capitalize()}-{data.get('country')}",
        "COUNTRY": f"{data.get('country')}-{data.get('region').lower().replace(' ', '_')}"
    }

    loguru.logger.debug(f"Greeting Request from {request.remote}")

    # Check if Client version is supported by server
    if sum(services.game_constants.MIN_CLIENT_VERSION) > sum(_json["client_version"]):
        return Codes.CLIENT_VERSION_TOO_LOW.to_response()
    
    res = {
        "id": UUID(secrets.token_hex(16)).hex,
        "version": services.game_constants.VERSION,
        "min_client_version": services.game_constants.MIN_CLIENT_VERSION,
        "region": region["SHORT"],
        "uptime": time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - services.uptime))
    }

    return web.json_response(res)


async def returning_greeting_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    id          = _json.get("id")
    auth_token  = _json.get("auth_token")

    loguru.logger.debug(f"Greeting Request from {request.remote}")

    # Get Authentication from Database
    # {
    #     "id": id,
    #     "auth_id": auth_id,
    #     "session_cert_model": certificate_model.to_dict(),
    #     "_timestamp": time.time()
    # }
    client_auth_params: CertificateModel | None = await services.redisdb.get(f"CLIENT::CERTIFICATE::{request.remote}::{id}", CertificateModel)
    if client_auth_params == None:
        loguru.logger.warning(Codes.DATABASE_RECORD_NOT_FOUND.to_logger())
        client_cert_model = await services.certificate_repository.get_certificate_by_auth_token(
            auth_token=auth_token
        )
        if client_cert_model == None: return Codes.DATABASE_RECORD_NOT_FOUND.to_response()
    
    if client_auth_params.auth_id != auth_token: return Codes.CLIENT_AUTHENTICATION_TOKEN_INVALID.to_response()

    # Generate new Authentication Token and ID
    new_id = UUID(secrets.token_hex(16))
    new_auth_token = hashlib.md5(new_id).hexdigest()


    # Update Clients Certificates with new Authentication Token and ID
    await services.redisdb.delete(f"CLIENT::CERTIFICATE::{request.remote}::{id}")
    await services.certificate_repository.delete_certificate(id)

    database_response = await services.certificate_repository.create_certificate(
        id=new_id,
        auth_id=new_auth_token,
        certificate=client_cert_model.certificate,
        private_key=client_cert_model.private_key,
        public_key=client_cert_model.public_key
    )
    if database_response == None: return Codes.DATABASE_QUERY_ERROR.to_response()

    await services.redisdb.add(f"CLIENT::CERTIFICATE::{request.remote}::{new_id}", CertificateModel.from_dict({
        "id": new_id,
        "auth_id": new_auth_token,
        "session_cert_model": database_response.to_dict()
    }))

    return web.json_response({
        "id": new_id,
        "auth_id": new_auth_token,
        "session_certificate": database_response.certificate
    })
    
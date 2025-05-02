import json, loguru
from aiohttp import web
from server.player.Account import Account
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def login_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    # Check if JSON is valid
    if _json.get("username") == None: return Codes.INVALID_FIELD_VALUE.to_response()
    if _json.get("email")    == None: return Codes.INVALID_FIELD_VALUE.to_response()
    if _json.get("pwd_hash") == None: return Codes.INVALID_FIELD_VALUE.to_response()

    username = _json.get("username")
    email    = _json.get("email")
    pwd_hash = _json.get("pwd_hash")

    loguru.logger.debug(f"Login Request for {username}@{request.remote}")

    account: Account = await services.account_repository.get_account_by_email(email)
    if account == None: return Codes.INTERNAL_SERVER_ERROR.to_response()

    if account.is_banned: return Codes.ACCOUNT_BANNED.to_response()

    res = {"status": "success"}
    res.update(account.to_client())
    return web.json_response(res)



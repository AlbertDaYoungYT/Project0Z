import json, loguru
from aiohttp import web
from database.models.CrashReportModel import CrashReportModel
from server.player.Account import Account
from utils.AppServices import AppServices
from utils.Errors import Codes  # Import the Router instance (see step 3)

async def crash_report_handler(request: web.Request, services: AppServices):
    _json: dict = json.loads(request.content.read_nowait())

    email    = _json.get("email")
    token    = _json.get("token")

    crash    = _json.get("crash_report")
    logcat   = _json.get("logcat_trail")

    account: Account = await services.account_repository.get_account_by_email(email)
    if account == None:
        account: Account = await services.account_repository.get_account_by_token(token)
        if account == None:
            loguru.logger.error(f"Oh uh... Server Failed to handle Client Error:")
            loguru.logger.error(f"CLIENT-{request.remote}: Email={email} Token={token} REQ={_json}")
            return web.json_response(Codes.FATAL_SERVER_ERROR.value.to_dict())


    if account.is_banned: return web.json_response(Codes.ACCOUNT_BANNED.value.to_dict())

    crash_report: CrashReportModel = await services.crash_report_repository.create_crash_report(account, crash, logcat)
    if crash_report == None: return web.json_response(Codes.INTERNAL_SERVER_ERROR.value.to_dict())

    loguru.logger.debug(f"CLIENT-{request.remote}: Crash report saved with id = {crash_report.report_id}")
    res = {"status": "success"}
    res.update({"reportId": crash_report.report_id})
    return web.json_response(res)
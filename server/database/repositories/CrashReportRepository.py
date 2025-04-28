
import secrets
from uuid import UUID
import loguru

from config.ConfigContainer import ConfigContainer
from database.DatabaseManager import CouchDBManager
from database.models.CrashReportModel import CrashReportModel
from server.player.Account import Account


class CrashReportRepository(CouchDBManager):

    def __init__(self, server_url: str, config: ConfigContainer):
        self.DATABASE_NAME = config.collection + "_crash_reports"
        super().__init__(server_url, config)

    async def create_crash_report(self, account: Account, crash_report: list[dict], logcat_report: list[dict]) -> CrashReportModel:
        """Create a new Crash Report."""
        doc = CrashReportModel(
            report_id=UUID(secrets.token_hex(16)),
            account_id=account.account_id,
            email=account.email,
            token=account.token,
            crash_report=crash_report,
            logcat_report=logcat_report
        )
        result = await self.save_document(self.DATABASE_NAME, doc.to_dict())
        if result:
            return doc
        return None
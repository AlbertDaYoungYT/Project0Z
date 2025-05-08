
import secrets
from uuid import UUID
import loguru

from config.ConfigContainer import ConfigContainer
from database.DatabaseManager import CouchDBManager
from database.Models import *
from server.player.Account import Account


class CrashReportRepository(CouchDBManager):

    def __init__(self, server: CouchDBManager, server_url: str, config: ConfigContainer):
        self.DATABASE_NAME = config.couchdb_collection + "_crash_reports"
        self.server_url = server_url
        self.config = config
        self.server = server

        self._link_to_cache(db=DataStores.CRASH_REPORT)
        loguru.logger.debug(f"Initiated CouchDB Repo: {self.DATABASE_NAME}")

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
        result = await self.server.save_document(self.DATABASE_NAME, doc.to_dict())
        if result:
            return doc
        return None
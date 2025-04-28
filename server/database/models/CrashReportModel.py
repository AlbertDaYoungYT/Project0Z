from dataclasses import dataclass
from uuid import UUID

from . import Model

@dataclass
class CrashReportModel(Model):
    report_id: UUID
    account_id: UUID
    email: str
    token: str

    crash_report: list[dict]
    logcat_report: list[dict]

import sys
import time
from GameConstants import GameConstants
from config.ConfigContainer import ConfigContainer
from database.repositories.AccountRepository import AccountRepository
from database.repositories.PlayerRepository import PlayerRepository
from database.repositories.CrashReportRepository import CrashReportRepository


class AppServices:
    def __init__(self):
        self.console_args = sys.argv[1:]
        self.uptime = time.time()

        self.game_server = None
        self.http_server = None
        self.game_constants = GameConstants

        self.config = ConfigContainer()
        self.account_repository = AccountRepository(self.config.connectionUri, self.config)
        self.player_repository = PlayerRepository(self.config.connectionUri, self.config)
        self.crash_report_repository = CrashReportRepository(self.config.connectionUri, self.config)
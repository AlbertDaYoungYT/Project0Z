
import sys
import time
from GameConstants import GameConstants
from config.ConfigContainer import ConfigContainer
from database.repositories.AccountRepository import AccountRepository
from database.repositories.PlayerRepository import PlayerRepository
from database.repositories.CrashReportRepository import CrashReportRepository
from database.repositories.CertificateRepository import CertificateRepository
from database.DatabaseManager import CouchDBManager, RedisDBManager
from security.DDOSProtection import DDOSProtectionSystem
from database.Models import *
from utils.registry import Registry
from task.TaskSystem import TaskScheduler
from utils.Crypto import CertificateAuthority, SessionKeyManager


class AppServices:

    # Registries
    asset_registry = Registry()

    def __init__(self, config: ConfigContainer, task_system: TaskScheduler):
        self.console_args = sys.argv[1:]
        self.uptime = time.time()
        self._keep_alive = True
        
        self.config: ConfigContainer = config
        self.task_system: TaskScheduler = task_system

        self.game_server = None
        self.http_server = None
        self.game_constants = GameConstants

        self.ca_authority = CertificateAuthority()
        self.session_key_manager = SessionKeyManager(self.ca_authority)

        # CouchDB Database
        self.couchdb = CouchDBManager(self.task_system, self.config.couchdb_connection_uri, self.config)
        self.account_repository = AccountRepository(self.couchdb, self.config.couchdb_connection_uri, self.config)
        self.player_repository = PlayerRepository(self.couchdb, self.config.couchdb_connection_uri, self.config)
        self.crash_report_repository = CrashReportRepository(self.couchdb, self.config.couchdb_connection_uri, self.config)
        self.certificate_repository = CertificateRepository(self.couchdb, self.config.couchdb_connection_uri, self.config)

        self.redisdb = RedisDBManager(self.config, db=DataStores.DEFAULT)

        self.ddos_protection_system = DDOSProtectionSystem(self.config)


        # The Registry instance 'asset_registry' is created at the class level.
        # If Registry.__init__ is modified to add itself to _global_registry, this line is not needed.
        # self.asset_registry.__init__("asset_registry") # This line is redundant and potentially problematic.


class VariableTunnel:
    def __init__(self):
        pass
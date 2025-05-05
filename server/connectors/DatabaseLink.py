

from dataclasses import dataclass



@dataclass
class DatabaseLinkConnector:

    redis: object
    couchdb: object
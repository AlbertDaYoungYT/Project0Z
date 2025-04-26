

from dataclasses import dataclass
from uuid import UUID

from server.sector.Sectors import Sector


@dataclass
class PlayerShip:
    ship_id: UUID
    ship_name: str
    ship_location: Sector

    #ship_inventory: Inventory
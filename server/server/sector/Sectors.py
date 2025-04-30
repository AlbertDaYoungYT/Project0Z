
from dataclasses import dataclass
from uuid import UUID

from .SectorBiome import SectorBiome
from server.sector.resources import *
from server.sector.structures.Defenses import Defenses
from server.sector.structures.Infrastructure import Infrastructure
from utils.Vectors import Vector2dPolygon


@dataclass
class Sector:
    sector_id: UUID
    sector_name: str
    sector_area: Vector2dPolygon
    sector_biome: SectorBiome
    
    max_health: float
    health: float
    regeneration_amount: float

    enemy_invasion_level: int
    missions_liberated: int
    missions_lost: int
    soldiers_fallen: int
    enemies_eradicated: int
    accidentals: int

    resources: List[Dict[Resource, int]]
    infrastructure: List[Infrastructure]
    defenses: List[Dict[Defenses, int]]
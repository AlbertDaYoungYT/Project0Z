
from dataclasses import dataclass
from enum import Enum

@dataclass
class ClimateType(Enum):
    ARID = "Arid"
    DESERT = "Desert"
    TROPICAL = "Tropical"
    TEMPERATE = "Temperate"
    FROZEN = "Frozen"
    MARINE = "Marine"
    MOUNTAINOUS = "Mountainous"
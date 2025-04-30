
from dataclasses import dataclass
from enum import Enum

from server.sector.climate.ClimateType import ClimateType
from utils.DatabaseAdapter import Serializable


@dataclass
class SectorBiome(Serializable):
    title: str
    description: str
    climate_type: ClimateType


@dataclass
class SectorBiomes(Enum):
    TROPICAL_RAINFOREST = SectorBiome("Tropical Rainforest", "Dense, warm forests near the equator with high rainfall; rich biodiversity.", ClimateType.TROPICAL)
    SAVANNA = SectorBiome("Savanna", "Grasslands with scattered trees found in regions like Africa; seasonal rainfall.", ClimateType.ARID)
    DESERT = SectorBiome("Desert", "Arid areas with sparse vegetation; extreme temperatures and low precipitation.", ClimateType.DESERT)
    CHAPARRAL = SectorBiome("Chaparral", "Shrubland biome with hot, dry summers and mild, wet winters; located in Mediterranean climates.", ClimateType.TEMPERATE)
    TEMPERATE_GRASSLANDS = SectorBiome("Temperate Grasslands", "Open plains dominated by grasses; experiences hot summers and cold winters.", ClimateType.TEMPERATE)
    TEMPERATE_DECIDUOUS_FOREST = SectorBiome("Temperate Deciduous Forest", "Forests in temperate zones that lose their leaves seasonally; moderate climate with well-distributed rainfall.", ClimateType.TEMPERATE)
    TAIGA = SectorBiome("Taiga", "Cold forests found in northern latitudes, dominated by conifers; long winters and short summers.", ClimateType.FROZEN)
    TUNDRA = SectorBiome("Tundra", "Treeless regions near the Arctic Circle or at high altitudes; cold temperatures with permafrost soil.", ClimateType.FROZEN)
    MONTANE = SectorBiome("Montane", "High elevation ecosystems above the tree line; cooler temperatures and unique flora/fauna adapted to altitude.", ClimateType.MOUNTAINOUS)
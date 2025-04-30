
from dataclasses import dataclass

from server.sector.terrain.Noise import Noise, PerlinNoise
from utils.DatabaseAdapter import Serializable


@dataclass
class Terrain(Serializable):
    """
    Represents terrain in-game.

    Attributes:
        vegetation_amount (float): The amount of vegetation in the terrain.
        structure_amount (float): The amount of structures in the terrain.
        amplification (float): The amplification factor for the terrain's height.
        size (tuple): The dimensions of the terrain.
        seed (int): A random seed for generating the terrain.
        max_height (int): The maximum height of the terrain.
        elevation_scale (float): The scale at which the terrain's elevation is determined.
        noise_type (str): The type of noise used to generate the terrain.
        frequency (float): The frequency at which the terrain's features are generated.
        roughness (float): A value controlling the terrain's roughness.
        texture_size (int): The size of textures in the terrain.
        water_depth (float): The maximum depth of water in the terrain.
        elevation_threshold (int): The minimum height required for a feature to be considered part of the terrain.
        noise_octaves (int): The number of octaves used in the noise function.
    """

    vegetation_amount: float
    structure_amount: float

    amplification: float

    size: tuple  # width, height
    seed: int
    max_height: int

    elevation_scale: float = 1.0
    noise_type: Noise = PerlinNoise()
    frequency: float = 100.0
    roughness: float = 0.5
    texture_size: int = 1024
    water_depth: float = 10.0
    elevation_threshold: int = 5
    noise_octaves: int = 6

    def __post_init__(self):
        """
        Post-initialization method to validate the seed value.
        """
        if not isinstance(self.seed, int) or self.seed < 0:
            raise ValueError("Seed must be a non-negative integer.")
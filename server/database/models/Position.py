

from dataclasses import dataclass

from . import Model


@dataclass
class Position(Model):
    """
    A dataclass representing a 3D position.  It uses a custom JSON adapter
    to handle serialization/deserialization.
    """
    x: float
    y: float
    z: float = 0.0  # Default value for z
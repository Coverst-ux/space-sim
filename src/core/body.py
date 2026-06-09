from dataclasses import dataclass 
from src.utils.vector import Vector2D

@dataclass
class Body:
    name: str
    mass: float
    position: Vector2D
    velocity: Vector2D
    radius: float = 1e9 
    color: tuple[int, int, int] = (255, 255, 255)
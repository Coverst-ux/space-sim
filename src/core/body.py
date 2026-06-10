from dataclasses import dataclass, field
from src.utils.vector import Vector2D

@dataclass
class Body:
    name: str
    mass: float
    position: Vector2D
    velocity: Vector2D
    radius: float = 1e9 
    color: tuple[int, int, int] = (255, 255, 255)
    # Default factory ensures every new Body gets its own fresh Vector2D(0,0)
    acceleration: Vector2D = field(default_factory=lambda: Vector2D(0, 0))
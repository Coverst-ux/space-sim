from dataclasses import dataclass, field
from src.utils.vector import Vector3D
from collections import deque

@dataclass
class Body:
    name: str
    mass: float
    position: Vector3D
    velocity: Vector3D
    radius: float = 1e9 
    color: tuple[int, int, int] = (255, 255, 255)
    acceleration: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 0))
    trail: deque = field(default_factory=lambda: deque(maxlen=500))
    def record_trail(self) -> None:
        self.trail.append((self.position.x, self.position.y, self.position.z))
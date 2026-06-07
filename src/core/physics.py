# src/core/physics.py
from src.utils.vector import Vector2D
from src.utils.constants import G

def gravitational_force(m1: float, m2: float, pos1: Vector2D, pos2: Vector2D) -> Vector2D:
    """Returns force vector acting on body 1 due to body 2."""
    displacement = Vector2D(pos2.x - pos1.x, pos2.y - pos1.y)
    distance = displacement.magnitude()
    if distance == 0:
        raise ValueError("Bodies occupy the same position")    
    magnitude = G * m1 * m2 / distance**2
    return displacement.normalized() * magnitude
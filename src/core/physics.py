# src/core/physics.py
from src.utils.constants import EPSILON
from src.utils.constants import G
from src.utils.vector import Vector2D


def gravitational_force(m1: float, m2: float, pos1: Vector2D, pos2: Vector2D) -> Vector2D:
    """Returns force vector acting on body 1 due to body 2."""
    displacement = Vector2D(pos2.x - pos1.x, pos2.y - pos1.y)
    distance = displacement.magnitude()
    if distance == 0:
        raise ValueError("Bodies occupy the same position")    
    magnitude = G * m1 * m2 / distance**2
    return displacement.normalized() * magnitude

def gravitational_force_softened(m1, m2, pos1, pos2):
    displacement = Vector2D(pos2.x - pos1.x, pos2.y - pos1.y)
    distance_sq = displacement.x**2 + displacement.y**2 + EPSILON**2
    magnitude = G * m1 * m2 / distance_sq
    return displacement.normalized() * magnitude
# src/core/physics.py
from src.core.body import Body
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

def check_and_merge(bodies: list[Body], merge_radius: float) -> list[Body]:
    merged = set()
    new_bodies = []
    for i, b1 in enumerate(bodies):
        if i in merged:
            continue
        for j, b2 in enumerate(bodies):
            if j <= i or j in merged:
                continue
            distance = (b2.position - b1.position).magnitude() 
            if distance < merge_radius:
                new_mass = b2.mass + b1.mass
                new_velocity = (b2.mass * b2.velocity + b1.mass * b1.velocity) * (1.0 /new_mass)
                b1.mass = new_mass
                b1.velocity = new_velocity
                merged.add(j)
        new_bodies.append(b1)
    return new_bodies
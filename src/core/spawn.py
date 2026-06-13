from src.core.body import Body
import math
import random

from src.utils.constants import G, SOLAR_MASS
from src.utils.vector import Vector2D

def generate_random_bodies(n:int)-> list[Body]:
    bodies = []
    total_mass = n * SOLAR_MASS

    for i in range(n):
        angle = random.uniform(0, 2 * math.pi) 
        r = random.uniform(1e10, 1e12)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        v_circ = math.sqrt(G * total_mass / r)
        vx = -v_circ * math.sin(angle)  # perpendicular to position
        vy =  v_circ * math.cos(angle)
        new_body = Body(
            name=f"body_{i}",
            mass=SOLAR_MASS,
            position=Vector2D(x, y),
            velocity=Vector2D(vx, vy)
        )
        bodies.append(new_body)

    return bodies
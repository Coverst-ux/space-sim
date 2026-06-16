from src.core.body import Body
import math
import random

from src.utils.constants import G, SOLAR_MASS
from src.utils.vector import Vector2D

def generate_random_bodies(n:int)-> list[Body]:
    bodies = []
    core_mass = SOLAR_MASS * n * 100
    core = Body(
        name="core",
        mass=core_mass,  # dominant central mass
        position=Vector2D(0, 0),
        velocity=Vector2D(0, 0)
    )
    bodies.append(core)

    for i in range(n):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(1e11, 1e12)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        v_circ = math.sqrt(G * core_mass / r)
        vx = -v_circ * math.sin(angle)  # perpendicular to position
        vy =  v_circ * math.cos(angle)
        r_norm = (r - 1e11) / (1e12 - 1e11)
        red = int(255 * (1 - r_norm))
        blue = int(255 * r_norm)
        new_body = Body(
            name=f"body_{i}",
            mass=SOLAR_MASS,
            position=Vector2D(x, y),
            velocity=Vector2D(vx, vy),
            color=(red,100,blue)
        )
        bodies.append(new_body)

    return bodies
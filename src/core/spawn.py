import space_sim_cpp
from src.rendering.render_body import RenderBody
import math
import random

from src.utils.constants import G, SOLAR_MASS


def generate_random_bodies(n: int):
    physics_bodies = space_sim_cpp.BodyVector()
    colors = []

    core_mass = SOLAR_MASS * n * 100
    core = space_sim_cpp.Body(
        "core", core_mass,
        space_sim_cpp.Vector3D(0, 0, 0),
        space_sim_cpp.Vector3D(0, 0, 0),
        1e9
    )
    physics_bodies.append(core)
    colors.append((255, 255, 255))

    for i in range(n):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(1e11, 1e12)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = random.gauss(0, 1e10)
        v_circ = math.sqrt(G * core_mass / r)
        vx = -v_circ * math.sin(angle)
        vy = v_circ * math.cos(angle)
        vz = 0
        r_norm = (r - 1e11) / (1e12 - 1e11)
        red = int(255 * (1 - r_norm))
        blue = int(255 * r_norm)

        new_body = space_sim_cpp.Body(
            f"body_{i}", SOLAR_MASS,
            space_sim_cpp.Vector3D(x, y, z),
            space_sim_cpp.Vector3D(vx, vy, vz),
            1e9
        )
        physics_bodies.append(new_body)
        colors.append((red, 100, blue))

    render_bodies = [RenderBody(physics_bodies[i], color=colors[i]) for i in range(len(physics_bodies))]
    return physics_bodies, render_bodies


def generate_spiral(n: int):
    physics_bodies = space_sim_cpp.BodyVector()
    colors = []

    core_mass = SOLAR_MASS * n * 500
    core = space_sim_cpp.Body(
        "core", core_mass,
        space_sim_cpp.Vector3D(0, 0, 0),
        space_sim_cpp.Vector3D(0, 0, 0),
        1e9
    )
    physics_bodies.append(core)
    colors.append((255, 255, 255))

    for i in range(n):
        arm = i % 2
        arm_base_angle = arm * math.pi
        theta = random.uniform(0, 4 * math.pi)
        min_r = 1e11
        max_r = 2e12
        r = min_r + (theta ** 0.85 / (4 * math.pi)) * (max_r - min_r)
        angle = theta + arm_base_angle + random.gauss(0, 0.3)
        x, y, z = r * math.cos(angle), r * math.sin(angle), random.gauss(0, 1e10)
        v_circ = math.sqrt(G * core_mass / r)
        vx = -v_circ * math.sin(angle)
        vy = v_circ * math.cos(angle)
        vz = 0
        r_norm = (r - min_r) / (max_r - min_r)
        red = int(255 * (1 - r_norm))
        green = int(150 * (1 - r_norm))
        blue = int(255 * r_norm)

        body = space_sim_cpp.Body(
            f"body_{i}", SOLAR_MASS,
            space_sim_cpp.Vector3D(x, y, z),
            space_sim_cpp.Vector3D(vx, vy, vz),
            1e9
        )
        physics_bodies.append(body)
        colors.append((red, green, blue))

    render_bodies = [RenderBody(physics_bodies[i], color=colors[i]) for i in range(len(physics_bodies))]
    return physics_bodies, render_bodies
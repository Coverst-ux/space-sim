import space_sim_cpp
from src.rendering.render_body import RenderBody
import math
import random
from src.core.body import Body
from src.utils.vector import Vector3D

from src.utils.constants import G, SOLAR_MASS


def generate_random_bodies(n: int): 
    # PROFILING/PERFORMANCE BENCHMARKING GENERATION
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



def generate_random_bodies_python(n: int): 
    # PROFILING/PERFORMANCE BENCHMARKING GENERATION
    physics_bodies = []
    colors = []

    core_mass = SOLAR_MASS * n * 100
    core = Body(
        "core", core_mass,
        Vector3D(0, 0, 0),
        Vector3D(0, 0, 0),
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

        new_body = Body(
            f"body_{i}", SOLAR_MASS,
            Vector3D(x, y, z),
            Vector3D(vx, vy, vz),
            1e9
        )
        physics_bodies.append(new_body)
        colors.append((red, 100, blue))

    return physics_bodies



def generate_spiral(n: int):
    # SIMULATION GENERATION
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


def generate_binary_white_dwarfs(m1, m2, position, separation):
    physics_bodies = space_sim_cpp.BodyVector()
    colors = []

    total_mass = m1 + m2
    d1 = separation * (m2 / total_mass)
    d2 =  separation * (m1 / total_mass)
    pos1 = position + space_sim_cpp.Vector3D(d1, 0, 0)
    pos2 = position - space_sim_cpp.Vector3D(d2, 0, 0)


    v_rel = math.sqrt(G * total_mass / separation)

    v1 = v_rel * (m2 / total_mass)
    v2 = v_rel * (m1 / total_mass)

    vel1 = space_sim_cpp.Vector3D(0, v1, 0)
    vel2 = space_sim_cpp.Vector3D(0, -v2, 0)
    binary_id=1
    radius = 6e6
    
    body1 = space_sim_cpp.Body("wd_1", m1, pos1, vel1, radius)
    body2 = space_sim_cpp.Body("wd_2", m2, pos2, vel2, radius)
    body1.stellar_type = space_sim_cpp.StellarType.WHITE_DWARF
    body2.stellar_type = space_sim_cpp.StellarType.WHITE_DWARF
    idx1=0
    idx2=1
    
    body1.binary_id = binary_id
    body2.binary_id = binary_id
    
    physics_bodies.append(body1)
    physics_bodies.append(body2)
    
    state = space_sim_cpp.create_binary_state(body1, body2, binary_id, idx1, idx2, m1, m2)
    
    colors.append((255, 255, 255))  # body1
    colors.append((200, 220, 255))  # body2 
    render_bodies = [RenderBody(physics_bodies[i], color=colors[i], trail_length=100) for i in range(len(physics_bodies))]
    return physics_bodies, render_bodies
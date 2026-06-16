import numpy as np
from src.core.quadtree import QuadNode
from src.utils.vector import Vector2D
from src.core.body import Body
from src.core.physics import gravitational_force_softened
from utils.constants import EPSILON, G


def euler_step(bodies: list[Body], dt: float) -> None:
    forces = {body.name: Vector2D(0,0) for body in bodies}
    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if i>=j:
                continue
            f = gravitational_force_softened(body1.mass, body2.mass, body1.position,  body2.position)
            
            forces[body1.name] = forces[body1.name] + f
            forces[body2.name] = forces[body2.name] + (f* -1)
            
    for body in bodies:
        acceleration = forces[body.name] * (1.0 / body.mass)
        old_velocity = body.velocity
        body.position = body.position + old_velocity * dt  
        body.velocity = body.velocity + acceleration * dt
                               
def update_forces(bodies: list[Body]) -> None:
    """Helper to calculate and assign accelerations to all bodies once."""
    forces = {body.name: Vector2D(0, 0) for body in bodies}
    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if i >= j:
                continue
            f = gravitational_force_softened(body1.mass, body2.mass, body1.position, body2.position)
            forces[body1.name] = forces[body1.name] + f
            forces[body2.name] = forces[body2.name] + (f * -1)

def update_forces_bh(bodies: list[Body], theta: float = 0.1) -> None:
    size = 1.0e13
    root = QuadNode(0,0,size)
    for body in bodies:
        root.insert(body)

    root.update_mass()

    for body in bodies:
        f = root.calculate_force(body, theta)
        body.acceleration = f * (1 / body.mass)

def update_forces_np(bodies: list[Body]):
    positions = np.array([[b.position.x, b.position.y] for b in bodies])
    masses = np.array([b.mass for b in bodies])

    diff_pos = positions[np.newaxis, :] - positions[:, np.newaxis]

    dist_sq = (diff_pos ** 2).sum(axis=2) + EPSILON ** 2
    dist = np.sqrt(dist_sq)
    force_mag = G * masses[:, np.newaxis] * masses[np.newaxis, :] / dist_sq
    force_vec = (force_mag / dist)[..., np.newaxis] * diff_pos
    total_force = force_vec.sum(axis=1)
    for i, body in enumerate(bodies):
        body.acceleration = Vector2D(float(total_force[i][0]), float(total_force[i][1])) * (1 / body.mass)


def leapfrog_step(bodies: list[Body], dt: float, is_first_step: bool = False) -> None:
    """
    Kick-Drift-Kick Leapfrog. 
    Requires tracking body.acceleration across steps to avoid double force calculation.
    """
    if is_first_step:
        update_forces_np(bodies)
        
    # 1. Kick: Update velocities by half a step using CURRENT accelerations
    for body in bodies:
        body.velocity = body.velocity + body.acceleration * (dt / 2.0)
        
    # 2. Drift: Update positions by a full step using NEW velocities
    for body in bodies:
        body.position = body.position + body.velocity * dt
        
    # 3. Update accelerations at the NEW positions
    update_forces_np(bodies)
    
    # 4. Kick: Update velocities by the remaining half step using NEW accelerations
    for body in bodies:
        body.velocity = body.velocity + body.acceleration * (dt / 2.0)
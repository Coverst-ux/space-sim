from src.utils.vector import Vector2D
from src.core.body import Body
from src.core.physics import gravitational_force

def euler_step(bodies: list[Body], dt: float) -> None:
    forces = {body.name: Vector2D(0,0) for body in bodies}
    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if i>=j:
                continue
            f = gravitational_force(body1.mass, body2.mass, body1.position,  body2.position)
            
            forces[body1.name] = forces[body1.name] + f
            forces[body2.name] = forces[body2.name] + (f* -1)
            
    for body in bodies:
        acceleration = forces[body.name] * (1.0 / body.mass)
        old_velocity = body.velocity
        body.position = body.position + old_velocity * dt  
        body.velocity = body.velocity + acceleration * dt
        
# In your Body class, make sure you have an attribute: self.acceleration = Vector2D(0, 0)

def update_forces(bodies: list[Body]) -> None:
    """Helper to calculate and assign accelerations to all bodies once."""
    forces = {body.name: Vector2D(0, 0) for body in bodies}
    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if i >= j:
                continue
            f = gravitational_force(body1.mass, body2.mass, body1.position, body2.position)
            forces[body1.name] = forces[body1.name] + f
            forces[body2.name] = forces[body2.name] + (f * -1)
            
    for body in bodies:
        body.acceleration = forces[body.name] * (1.0 / body.mass)

def leapfrog_step(bodies: list[Body], dt: float, is_first_step: bool = False) -> None:
    """
    Kick-Drift-Kick Leapfrog. 
    Requires tracking body.acceleration across steps to avoid double force calculation.
    """
    # If it's the very first step of the simulation, we need initial accelerations
    if is_first_step:
        update_forces(bodies)
        
    # 1. Kick: Update velocities by half a step using CURRENT accelerations
    for body in bodies:
        body.velocity = body.velocity + body.acceleration * (dt / 2.0)
        
    # 2. Drift: Update positions by a full step using NEW velocities
    for body in bodies:
        body.position = body.position + body.velocity * dt
        
    # 3. Update accelerations at the NEW positions
    update_forces(bodies)
    
    # 4. Kick: Update velocities by the remaining half step using NEW accelerations
    for body in bodies:
        body.velocity = body.velocity + body.acceleration * (dt / 2.0)
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
        body.velocity = body.velocity + acceleration * dt
        body.position = body.position + body.velocity * dt  
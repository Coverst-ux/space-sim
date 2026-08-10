import math

import pytest

from src.core.body import Body
from src.core.integrator import leapfrog_step
from src.core.physics import check_and_merge, gravitational_force_softened
from src.core.spawn import generate_random_bodies_python
from src.io.loader import config_loader_python
from src.utils.constants import G
from src.utils.vector import Vector3D


def test_gravitational_force_softened():
    pos1 = Vector3D(0, 0, 0)
    pos2 = Vector3D(1, 0, 0)
    f = gravitational_force_softened(1.0, 1.0, pos1, pos2)
    assert abs(f.magnitude()- 6.6743e-29 ) < 1e-32
    
def test_gravity_zero_distance_raises():
    with pytest.raises(ValueError):
        gravitational_force_softened(1.0, 1.0, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
        
def test_earth_orbital_period():
    bodies = config_loader_python()
    sun = bodies[0]
    earth = bodies[1]
    dx = earth.position.x - sun.position.x
    dy = earth.position.y - sun.position.y
    theta = math.atan2(dy,dx)
    dt = 3600
    steps = 8766
    for step in range(steps):
        leapfrog_step(bodies, dt)
    dx = earth.position.x - sun.position.x
    dy = earth.position.y - sun.position.y
    theta_after = math.atan2(dy,dx)
    
    assert theta_after - theta < 0.05

def  test_total_momentum():
    b1 = Body(name="b1", mass=1e24, position=Vector3D(0, 0, 0), velocity=Vector3D(100, 0, 0))
    b2 = Body(name="b2", mass=2e24, position=Vector3D(500, 0, 0), velocity=Vector3D(-50, 0, 0))
    merge_radius = 1000
    px_before = b1.mass * b1.velocity.x + b2.mass * b2.velocity.x + b2.mass * b2.velocity.z
    py_before = b1.mass * b1.velocity.y + b2.mass * b2.velocity.y + b2.mass * b2.velocity.z
    pz_before = b1.mass * b1.velocity.z + b2.mass * b2.velocity.z 
    result = check_and_merge([b1, b2], merge_radius)
    px_after = sum(b.mass * b.velocity.x for b in result)
    py_after = sum(b.mass * b.velocity.y for b in result)
    pz_after = sum(b.mass * b.velocity.z for b in result)
    assert abs(px_after - px_before) < 1e15
    assert abs(py_after - py_before) < 1e15
    assert abs(pz_after - pz_before) < 1e15



def test_generate_random_bodies_output():
    """Verify that the generation creates the right number of valid Body objects."""
    n = 50
    bodies = generate_random_bodies_python(n)
    
    # 1. Check total count
    assert len(bodies) == n
    
    # 2. Check types and properties of the generated bodies
    for i, body in enumerate(bodies):
        assert isinstance(body, Body)
        assert body.name == f"body_{i}"
        
        # 3. Verify positions are within the expected disk boundaries (1e10 to 1e12 meters)
        # We find the magnitude (radius) of the position vector
        pos_magnitude = math.sqrt(body.position.x**2 + body.position.y**2 + body.position.z**2)
        assert 1e10 <= pos_magnitude <= 1e12
        
        # 4. Verify velocities are non-zero and matching orbital expectations
        vel_magnitude = math.sqrt(body.velocity.x**2 + body.velocity.y**2 + body.velocity.z**2)
        assert vel_magnitude > 0


def test_collision_merging_conserves_momentum() -> None:
    body1 = Body(
        name="planet_1",
        mass=1000.0,
        position = Vector3D(0.0, 0.0, 0.0),
        velocity=Vector3D(100.0, 0.0, 0.0)
    )

    body2 = Body(
        name="planet_2",
        mass=2000.0,
        position=Vector3D(10.0, 0.0, 0.0),
        velocity=Vector3D(-50.0, 0.0, 0.0)
    )

    bodies = [body1, body2]

    initial_momentum_x = (body1.mass * body1.velocity.x) + (body2.mass * body2.velocity.x)
    initial_momentum_y = (body1.mass * body1.velocity.y) + (body2.mass * body2.velocity.y)
    initial_momentum_z = (body1.mass * body1.velocity.z) + (body2.mass * body2.velocity.z)

    remaining_bodies = check_and_merge(bodies, merge_radius=15.0)
    assert len(remaining_bodies) == 1

    final_body = remaining_bodies[0]

    final_momentum_x = final_body.mass * final_body.velocity.x
    final_momentum_y = final_body.mass * final_body.velocity.y
    final_momentum_z = final_body.mass * final_body.velocity.z

    assert final_momentum_x == pytest.approx(initial_momentum_x)
    assert final_momentum_y == pytest.approx(initial_momentum_y)
    assert final_momentum_z == pytest.approx(initial_momentum_z)
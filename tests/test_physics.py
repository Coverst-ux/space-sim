import math

import pytest

from src.core.body import Body
from src.core.integrator import leapfrog_step
from src.core.physics import check_and_merge, gravitational_force
from src.io.loader import config_loader
from src.utils.constants import G
from src.utils.vector import Vector2D


def test_gravitational_force():
    pos1 = Vector2D(0,0)
    pos2 = Vector2D(1,0)
    f = gravitational_force(1.0, 1.0, pos1, pos2)
    assert abs(f.magnitude()- G ) < 1e-20
    
def test_gravity_zero_distance_raises():
    with pytest.raises(ValueError):
        gravitational_force(1.0, 1.0, Vector2D(0,0), Vector2D(0,0))
        
def test_earth_orbital_period():
    bodies = config_loader()
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
    b1 = Body(name="b1", mass=1e24, position=Vector2D(0, 0), velocity=Vector2D(100, 0))
    b2 = Body(name="b2", mass=2e24, position=Vector2D(500, 0), velocity=Vector2D(-50, 0))
    merge_radius = 1000
    px_before = b1.mass * b1.velocity.x + b2.mass * b2.velocity.x
    py_before = b1.mass * b1.velocity.y + b2.mass * b2.velocity.y
    result = check_and_merge([b1, b2], merge_radius)
    px_after = sum(b.mass * b.velocity.x for b in result)
    py_after = sum(b.mass * b.velocity.y for b in result)
    assert abs(px_after - px_before) < 1e15
    assert abs(py_after - py_before) < 1e15
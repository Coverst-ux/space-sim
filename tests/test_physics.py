import pytest
import math
from src.utils.vector import Vector2D
from src.core.physics import gravitational_force
from src.utils.constants import G
from src.core.integrator import leapfrog_step
from src.io.loader import config_loader

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
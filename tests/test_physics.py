import pytest
from src.utils.vector import Vector2D
from src.core.physics import gravitational_force
from src.utils.constants import G

def test_gravitational_force():
    pos1 = Vector2D(0,0)
    pos2 = Vector2D(1,0)
    f = gravitational_force(1.0, 1.0, pos1, pos2)
    assert abs(f.magnitude()- G ) < 1e-20
    
def test_gravity_zero_distance_raises():
    with pytest.raises(ValueError):
        gravitational_force(1.0, 1.0, Vector2D(0,0), Vector2D(0,0))
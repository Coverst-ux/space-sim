import pytest
import math
from src.utils.vector import Vector3D


def test_addition():
    result = Vector3D(3, 4, 5) + Vector3D(1, 2, 3)
    assert result.x == 4
    assert result.y == 6
    assert result.z == 8

def test_multiplication():
    result = Vector3D(1, 2, 3) * 3
    assert result.x == 3
    assert result.y == 6
    assert result.z == 9
    
def test_magnitude():
    result = Vector3D(3, 4, 5)
    assert  abs(result.magnitude() - math.sqrt(50)) < 1e-9
    
def test_normalization():
    result = Vector3D(3, 4, 5).normalized()
    assert abs(result.magnitude()- 1.0) < 1e-9
    
def test_zero_vector():
    with pytest.raises(ValueError):
        Vector3D(0, 0, 0).normalized()
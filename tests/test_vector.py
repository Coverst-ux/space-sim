import pytest
from src.utils.vector import Vector2D


def test_addition():
    result = Vector2D(3,4) + Vector2D(1,2)
    assert result.x == 4
    assert result.y == 6

def test_multiplication():
    result = Vector2D(1,2) * 3
    assert result.x == 3
    assert result.y == 6
    
def test_magnitude():
    result = Vector2D(3,4)
    assert  abs(result.magnitude() - 5.0) < 1e-9
    
def test_normalization():
    result = Vector2D(3, 4).normalized()
    assert abs(result.magnitude()- 1.0) < 1e-9
    
def test_zero_vector():
    with pytest.raises(ValueError):
        Vector2D(0, 0).normalized()
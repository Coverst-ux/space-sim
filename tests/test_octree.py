import pytest

from core.body import Body
from core.octree import OctNode
from utils.vector import Vector3D


def test_get_octant():
    node = OctNode(0, 0, 0, 1e13)
    body = Body(name="test", mass=1e30, position=Vector3D(1, 1, 1), velocity=Vector3D(0, 0, 0))
    assert node.get_octant(body.position) == 7

def test_update_mass():
    body1 = Body(name="test1", mass=1e30, position=Vector3D(1e11, 0, 0), velocity=Vector3D(0, 0, 0))
    body2 = Body(name="test2", mass=1e30, position=Vector3D(-1e11, 0, 0), velocity=Vector3D(0, 0, 0))
    node = OctNode(0, 0, 0, 1e13)
    node.insert(body1)
    node.insert(body2)
    node.update_mass()
    assert node.total_mass == body1.mass + body2.mass

def test_calculate_force():
    body1 = Body(name="test1", mass=1e30, position=Vector3D(1e11, 0, 0), velocity=Vector3D(0, 0, 0))
    body2 = Body(name="test2", mass=1e30, position=Vector3D(-1e11, 0, 0), velocity=Vector3D(0, 0, 0))
    node = OctNode(0, 0, 0, 1e13)
    node.insert(body1)
    node.insert(body2)
    node.update_mass()
    force = node.calculate_force(body1, theta= 0.5)
    assert force.magnitude() > 0

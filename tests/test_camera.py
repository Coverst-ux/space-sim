import math

from src.rendering.camera import Camera


def test_world_to_screen_returns_none_for_non_finite_coordinates():
    camera = Camera(800, 800)

    assert camera.world_to_screen(float("nan"), 0.0, 0.0) is None
    assert camera.world_to_screen(float("inf"), 0.0, 0.0) is None
    assert camera.world_to_screen(-float("inf"), 0.0, 0.0) is None


def test_world_to_screen_returns_tuple_for_finite_coordinates():
    camera = Camera(800, 800)

    result = camera.world_to_screen(0.0, 0.0, 0.0)

    assert result == (400, 400)

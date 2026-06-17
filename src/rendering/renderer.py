from src.utils.vector import Vector3D


def world_to_screen(pos: Vector3D, scale: float, offset: tuple) -> tuple[int, int]:
    screen_x = int(pos.x * scale + offset[0])
    screen_y = int(pos.y * scale + offset[1])
    return screen_x, screen_y
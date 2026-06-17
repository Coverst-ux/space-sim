import math

class Camera:
    def __init__(self, screen_w: int, screen_h: int):
        self.offset_x = screen_w // 2
        self.offset_y = screen_h // 2
        self.zoom = 1.0
        self.azimuth= 0
        self.elevation= math.pi / 2

    def world_to_screen(self, wx, wy, wz):
        px, py = self.project(wx, wy, wz)
        sx = int(px * self.zoom + self.offset_x)
        sy = int(py * self.zoom + self.offset_y)
        return sx, sy
    
    def zoom_in(self, factor: float = 1.1): self.zoom *= factor
    def zoom_out(self, factor: float = 1.1): self.zoom /= factor
    def project(self, wx, wy, wz):
        screen_x = wx * math.cos(self.azimuth) - wy * math.sin(self.azimuth)
        screen_y = (wx * math.sin(self.azimuth) + wy * math.cos(self.azimuth)) * math.sin(
            self.elevation) - wz * math.cos(self.elevation)
        return screen_x, screen_y

    def rotate_azimuth(self, angle: float): self.azimuth += angle
    def rotate_elevation(self, angle: float): self.elevation += angle
    def pan(self, dx: int, dy: int):
        self.offset_x += dx
        self.offset_y += dy


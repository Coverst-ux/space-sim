class Camera:
    def __init__(self, screen_w: int, screen_h: int):
        self.offset_x = screen_w // 2
        self.offset_y = screen_h // 2
        self.zoom = 1.0
    
    def world_to_screen(self, wx: float, wy:float) ->tuple[int,int]:
        sx = int(wx * self.zoom + self.offset_x)
        sy = int(wy * self.zoom + self.offset_y)
        return sx,sy
    
    def zoom_in(self, factor: float = 1.1): self.zoom *= factor
    def zoom_out(self, factor: float = 1.1): self.zoom /= factor
    def pan(self, dx: int, dy: int):
        self.offset_x += dx
        self.offset_y += dy
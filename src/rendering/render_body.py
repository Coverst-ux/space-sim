from collections import deque

class RenderBody:
    def __init__(self, cpp_body, color=(255, 255, 255), trail_length=500):
        self.cpp_body = cpp_body
        self.color = color
        self.trail = deque(maxlen=trail_length)

    @property
    def position(self):
        return self.cpp_body.position

    @property
    def velocity(self):
        return self.cpp_body.velocity

    @property
    def name(self):
        return self.cpp_body.name

    def record_trail(self):
        p = self.cpp_body.position
        self.trail.append((p.x, p.y, p.z))
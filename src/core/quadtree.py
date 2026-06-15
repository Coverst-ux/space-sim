import math

from core.physics import gravitational_force_softened
from utils.vector import Vector2D


class QuadNode:
    def __init__(self, cx, cy, size):
        self.cx = cx
        self.cy = cy
        self.size = size
        self.body = None
        self.total_mass = 0
        self.center_of_mass_x = 0
        self.center_of_mass_y = 0
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
    def insert(self, body):
        
        if self.body is None and self.nw is None:
            self.body = body
            return
        if self.body and self.nw is None:
            if self.size < 1e6:
                return
            old_body = self.body
            self.body = None
            self.subdivide()
            quadrant = self.get_quadrant(body)
            quadrant_old = self.get_quadrant(old_body)
            if quadrant_old is not None:
                quadrant_old.insert(old_body)
            if quadrant is not None:
                quadrant.insert(body)
        if self.body is None and self.nw is not None:
            quadrant = self.get_quadrant(body)
            if quadrant is not None:
                quadrant.insert(body)

    def subdivide(self):
        self.ne = QuadNode(
            self.cx + self.size / 4, self.cy + self.size / 4, self.size / 2
        )
        self.nw = QuadNode(
            self.cx - self.size / 4, self.cy + self.size / 4, self.size / 2
        )
        self.se = QuadNode(
            self.cx + self.size / 4, self.cy - self.size / 4, self.size / 2
        )
        self.sw = QuadNode(
            self.cx - self.size / 4, self.cy - self.size / 4, self.size / 2
        )

    def get_quadrant(self, body):
        if body.position.x >= self.cx and body.position.y >= self.cy:
            return self.ne
        elif body.position.x < self.cx and body.position.y >= self.cy:
            return self.nw
        elif body.position.x >= self.cx and body.position.y < self.cy:
            return self.se
        elif body.position.x < self.cx and body.position.y < self.cy:
            return self.sw

    def update_mass(self):
        if self.body and self.ne is None:
            self.total_mass = self.body.mass
            self.center_of_mass_x = self.body.position.x
            self.center_of_mass_y = self.body.position.y
            return
        self.total_mass = 0
        self.center_of_mass_x = 0
        self.center_of_mass_y = 0
        
        children = [self.nw, self.ne, self.sw, self.se]

        for child in children:
            if child is not None:
                child.update_mass()
        for child in children:
            if child is not None and child.total_mass > 0:
                self.total_mass += child.total_mass
                self.center_of_mass_x += child.total_mass * child.center_of_mass_x
                self.center_of_mass_y += child.total_mass * child.center_of_mass_y
                
        if self.total_mass > 0:
            self.center_of_mass_x = self.center_of_mass_x / self.total_mass
            self.center_of_mass_y = self.center_of_mass_y / self.total_mass

        return
    def calculate_force(self, body, theta):
        if self.body is not None and self.nw is None:
            if self.body is body:
                return Vector2D(0, 0)
            return gravitational_force_softened(body.mass, self.body.mass, body.position, self.body.position)

        d = math.sqrt((body.position.x - self.center_of_mass_x) ** 2 + (body.position.y - self.center_of_mass_y) ** 2)
        if d == 0:
            return Vector2D(0, 0)
        if self.size / d < theta:
            return gravitational_force_softened(body.mass, self.total_mass, body.position, Vector2D(self.center_of_mass_x, self.center_of_mass_y))

        children = [self.nw, self.ne, self.sw, self.se]
        init_force = Vector2D(0, 0)
        for child in children:
            if child is not None:
                init_force +=  child.calculate_force(body, theta)
        return init_force



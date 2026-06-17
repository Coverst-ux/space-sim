import math
from src.core.physics import gravitational_force_softened
from src.utils.vector import Vector3D


class OctNode:
    def __init__(self, cx, cy, cz, size):
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.size = size
        self.body = None
        self.total_mass = 0.0
        self.center_of_mass_x = 0.0
        self.center_of_mass_y = 0.0
        self.center_of_mass_z = 0.0
        self.children = [None] * 8

    def insert(self, body):
        if self.body is None and self.children[0] is None:
            self.body = body
            return
        elif self.body is not None and self.children[0] is None:

            old_body = self.body
            self.body = None
            self.subdivide()

            old_idx = self.get_octant(old_body.position)
            idx = self.get_octant(body.position)

            self.children[old_idx].insert(old_body)
            self.children[idx].insert(body)
        else:
            idx = self.get_octant(body.position)
            self.children[idx].insert(body)

    def subdivide(self):
        offset = self.size / 4.0
        for idx in range(8):
            x_offset = offset if (idx & 1) else -offset
            y_offset = offset if (idx & 2) else -offset
            z_offset = offset if (idx & 4) else -offset
            self.children[idx] = OctNode(self.cx + x_offset, self.cy + y_offset, self.cz + z_offset, self.size / 2.0)

    def get_octant(self, position):
        idx = 0
        if position.x >= self.cx:
            idx |= 1
        if position.y >= self.cy:
            idx |= 2
        if position.z >= self.cz:
            idx |= 4
        return idx

    def update_mass(self):
        if self.body and self.children[0] is None:
            self.total_mass = self.body.mass
            self.center_of_mass_x = self.body.position.x
            self.center_of_mass_y = self.body.position.y
            self.center_of_mass_z = self.body.position.z
            return

        self.total_mass = 0.0
        self.center_of_mass_x = 0.0
        self.center_of_mass_y = 0.0
        self.center_of_mass_z = 0.0

        for child in self.children:
            if child is not None:
                child.update_mass()
                if child.total_mass > 0:
                    self.total_mass += child.total_mass
                    self.center_of_mass_x += child.total_mass * child.center_of_mass_x
                    self.center_of_mass_y += child.total_mass * child.center_of_mass_y
                    self.center_of_mass_z += child.total_mass * child.center_of_mass_z

        if self.total_mass > 0:
            self.center_of_mass_x /= self.total_mass
            self.center_of_mass_y /= self.total_mass
            self.center_of_mass_z /= self.total_mass

    def calculate_force(self, body, theta):
        if self.body is not None and self.children[0] is None:
            if self.body is body:
                return Vector3D(0, 0, 0)
            return gravitational_force_softened(body.mass, self.body.mass, body.position, self.body.position)

        d = math.sqrt((body.position.x - self.center_of_mass_x) ** 2 +
                      (body.position.y - self.center_of_mass_y) ** 2 +
                      (body.position.z - self.center_of_mass_z) ** 2)
        if d == 0:
            return Vector3D(0, 0, 0)

        if self.size / d < theta:
            return gravitational_force_softened(
                body.mass, self.total_mass, body.position,
                Vector3D(self.center_of_mass_x, self.center_of_mass_y, self.center_of_mass_z)
            )

        init_force = Vector3D(0, 0, 0)
        for child in self.children:
            if child is not None:
                init_force = init_force + child.calculate_force(body, theta)
        return init_force
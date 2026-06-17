import math

class Vector3D:
    def __init__ (self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalized(self) -> 'Vector3D':
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Can't normalize a zero vector")
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)
        
    def dot(self, other: 'Vector3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3D') -> 'Vector3D':
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        return Vector3D(cx, cy, cz)

    def __repr__(self):
        return f"Vector3D({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"
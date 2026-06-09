import math

class Vector2D:
    def __init__ (self, x: float, y: float):
        self.x = x
        self.y = y
        
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalized(self) -> 'Vector2D':
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Can't normalize a zero vector")
        return Vector2D(self.x / mag, self.y / mag)
        
    def dot(self, other: 'Vector2D') -> float:
        return self.x * other.x + self.y * other.y
    
    def __repr__(self):
        return f"Vector2D({self.x:.4f}, {self.y:.4f})"
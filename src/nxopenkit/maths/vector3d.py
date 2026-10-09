import math
from typing import Union
import NXOpen
Number = Union[int, float]
class Vector3d:
    def __init__(self, x: Number, y: Number, z: Number):
        if not all(isinstance(coord, (int, float)) for coord in (x, y, z)):
            raise TypeError("Coordinates must be numeric values.")
        if not all(math.isfinite(coord) for coord in (x, y, z)):
            raise ValueError("Coordinates must be finite numbers.")
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Vector3d({self.x}, {self.y}, {self.z})"

    @property
    def to_nx(self) -> NXOpen.Vector3d:
        return  NXOpen.Vector3d(float(self.x), float(self.y), float(self.z))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other: "Vector3d") -> "Vector3d":
        if not isinstance(other, Vector3d):
            return NotImplemented
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3d") -> "Vector3d":
        if not isinstance(other, Vector3d):
            return NotImplemented
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> "Vector3d":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector3d(self.x * scalar, self.y * scalar, self.z * scalar)

    def cross(self, other: "Vector3d") -> "Vector3d":
        if not isinstance(other, Vector3d):
            return NotImplemented
        return Vector3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def dot(self, other: "Vector3d") -> float:
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self) -> "Vector3d":
        magnitude = self.magnitude()
        if magnitude == 0:
            raise ValueError("Cannot normalize the zero vector.")
        return Vector3d(self.x / magnitude, self.y / magnitude, self.z / magnitude)

    def angle_with(self, other: "Vector3d") -> float:
        if not isinstance(other, Vector3d):
            return NotImplemented
        dot_product = self.dot(other)
        magnitude_product = self.magnitude() * other.magnitude()
        if magnitude_product == 0:
            raise ValueError("Cannot compute angle with the zero vector.")
        return math.acos(dot_product / magnitude_product)

    def parallel_to(self, other: "Vector3d") -> bool:
        if not isinstance(other, Vector3d):
            return NotImplemented
        cross_product = self.cross(other)
        return cross_product.magnitude() == 0

    def collinear_with(self, other: "Vector3d") -> bool:
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.parallel_to(other) and self.dot(other) > 0

    def perpendicular_to(self, other: "Vector3d") -> bool:
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.dot(other) == 0

    
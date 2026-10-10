import math

import NXOpen
from .vector3d import Vector3d
from typing import Union
Number = Union[int, float]

class Point3d:
    def __init__(self, x: Number, y: Number, z: Number):
        if not all(isinstance(coord, (int, float)) for coord in (x, y, z)):
            raise TypeError("Coordinates must be numeric values.")
        if not all(math.isfinite(coord) for coord in (x, y, z)):
            raise ValueError("Coordinates must be finite numbers.")
        self.x = x
        self.y = y
        self.z = z

    @property
    def to_nx(self) -> NXOpen.Point3d:
        return NXOpen.Point3d(float(self.x), float(self.y), float(self.z))

    def __str__(self):
        return f"Point3d({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point3d):
            return NotImplemented
        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )

    def equals(self, other, round_digit=8):
        if not isinstance(other, Point3d):
            return NotImplemented
        tol = 10 ** (-round_digit)
        return (
            abs(self.x - other.x) <= tol and
            abs(self.y - other.y) <= tol and
            abs(self.z - other.z) <= tol
        )

    def __add__(self, other: "Point3d") -> "Point3d":
        if not isinstance(other, Point3d):
            return NotImplemented
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Point3d") -> "Point3d":
        if not isinstance(other, Point3d):
            return NotImplemented
        return Point3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Point3d":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Point3d(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> "Point3d":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return Point3d(self.x / scalar, self.y / scalar, self.z / scalar)

    def __div__(self, scalar: float) -> "Point3d":
        return self.__truediv__(scalar)

    def distance_to(self, other: "Point3d") -> float:
        if not isinstance(other, Point3d):
            return NotImplemented
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    def midpoint(self, other: "Point3d") -> "Point3d":
        if not isinstance(other, Point3d):
            return NotImplemented
        return Point3d((self.x + other.x) / 2, (self.y + other.y) / 2, (self.z + other.z) / 2)

    def to_vector(self) -> "Vector3d":
        from .vector3d import Vector3d  # Import here to avoid circular import
        return Vector3d(self.x, self.y, self.z)

    def translate(self, vector: "Vector3d") -> "Point3d":
        if not isinstance(vector, Vector3d):
            return NotImplemented
        return Point3d(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def scale(self, factor: float) -> "Point3d":
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Point3d(self.x * factor, self.y * factor, self.z * factor)

    def to_tuple(self) -> tuple:
        return (self.x, self.y, self.z)

    def to_list(self) -> list:
        return [self.x, self.y, self.z]

    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}

    def is_origin(self) -> bool:
        return self.x == 0 and self.y == 0 and self.z == 0

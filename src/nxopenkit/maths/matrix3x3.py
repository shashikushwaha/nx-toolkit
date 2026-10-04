import math

try:
    import NXOpen
except ImportError:  # pragma: no cover - handled in environments without NXOpen
    NXOpen = None


class Matrix3X3:
    _ATTRS = ("Xx", "Xy", "Xz", "Yx", "Yy", "Yz", "Zx", "Zy", "Zz")

    def __init__(self, *values):
        if len(values) == 1 and hasattr(values[0], "Xx"):
            matrix = values[0]
            values = tuple(getattr(matrix, attr) for attr in self._ATTRS)
        elif len(values) == 1 and isinstance(values[0], (list, tuple)):
            values = tuple(values[0])

        if len(values) != 9:
            raise TypeError("Matrix3X3 expects either 9 numeric values or a Matrix3X3-like object.")

        if not all(isinstance(value, (int, float)) for value in values):
            raise TypeError("Matrix3X3 values must be numeric.")

        if not all(math.isfinite(value) for value in values):
            raise ValueError("Matrix3X3 values must be finite numbers.")

        self.Xx, self.Xy, self.Xz, self.Yx, self.Yy, self.Yz, self.Zx, self.Zy, self.Zz = values
        self.nx_matrix = None

    @property
    def to_nx(self):
        if NXOpen is None or not hasattr(NXOpen, "Matrix3X3"):
            return self
        if self.nx_matrix is None:
            self.nx_matrix = NXOpen.Matrix3X3(
                self.Xx, self.Xy, self.Xz,
                self.Yx, self.Yy, self.Yz,
                self.Zx, self.Zy, self.Zz,
            )
        return self.nx_matrix

    def __str__(self):
        return f"Matrix3X3(\n  {self.Xx}, {self.Xy}, {self.Xz}\n  {self.Yx}, {self.Yy}, {self.Yz}\n  {self.Zx}, {self.Zy}, {self.Zz}\n)"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other, rounding_precision: int = 6):
        if not isinstance(other, Matrix3X3):
            return NotImplemented
        return all(
            round(getattr(self, attr), rounding_precision) == round(getattr(other, attr), rounding_precision)
            for attr in self._ATTRS
        )

import math
import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxopenkit.maths.vector3d import Vector3d

try:
    import NXOpen  # noqa: F401
except Exception as exc:  # pragma: no cover
    pytest.skip(f"NXOpen unavailable or incompatible in this environment: {exc}", allow_module_level=True)




@pytest.fixture
def sample_vectors():
    return Vector3d(1, 2, 3), Vector3d(4, 5, 6)


class TestVector3d:
    def test_repr(self, sample_vectors):
        vector, _ = sample_vectors
        assert repr(vector) == "Vector3d(1, 2, 3)"

    def test_to_nx(self, sample_vectors):
        vector, _ = sample_vectors
        with patch("nxopenkit.maths.vector3d.NXOpen") as nxopen:
            nx_vector = vector.to_nx
        assert nx_vector is nxopen.Vector3d.return_value
        nxopen.Vector3d.assert_called_once_with(1, 2, 3)

    def test_equality(self, sample_vectors):
        vector, other = sample_vectors
        assert vector == Vector3d(1, 2, 3)
        assert vector != other
        assert vector.__eq__(object()) is NotImplemented

    def test_addition(self, sample_vectors):
        vector, other = sample_vectors
        assert vector + other == Vector3d(5, 7, 9)
        assert vector.__add__(object()) is NotImplemented

    def test_subtraction(self, sample_vectors):
        vector, other = sample_vectors
        assert vector - other == Vector3d(-3, -3, -3)
        assert vector.__sub__(object()) is NotImplemented

    def test_multiplication(self, sample_vectors):
        vector, _ = sample_vectors
        assert vector * 2 == Vector3d(2, 4, 6)
        assert vector * 0.5 == Vector3d(0.5, 1, 1.5)
        assert vector.__mul__("2") is NotImplemented

    def test_cross_product(self, sample_vectors):
        vector, other = sample_vectors
        assert vector.cross(other) == Vector3d(-3, 6, -3)
        assert vector.cross(object()) is NotImplemented

    def test_dot_product(self, sample_vectors):
        vector, other = sample_vectors
        assert vector.dot(other) == 32
        assert vector.dot(object()) is NotImplemented

    def test_magnitude(self, sample_vectors):
        vector, _ = sample_vectors
        assert math.isclose(vector.magnitude(), math.sqrt(14))
        assert Vector3d(0, 0, 0).magnitude() == 0

    def test_normalize(self, sample_vectors):
        vector, _ = sample_vectors
        normalized = vector.normalize()
        assert math.isclose(normalized.magnitude(), 1)
        with pytest.raises(ValueError, match="Cannot normalize the zero vector"):
            Vector3d(0, 0, 0).normalize()

    def test_finite_coordinates(self):
        with pytest.raises(ValueError, match="Coordinates must be finite numbers"):
            Vector3d(float("inf"), 0, 0)
        with pytest.raises(ValueError, match="Coordinates must be finite numbers"):
            Vector3d(0, float("nan"), 0)

    def test_angle_with(self, sample_vectors):
        vector, _ = sample_vectors
        assert math.isclose(Vector3d(1, 0, 0).angle_with(Vector3d(0, 1, 0)), math.pi / 2)
        with pytest.raises(ValueError, match="Cannot compute angle with the zero vector"):
            vector.angle_with(Vector3d(0, 0, 0))
        assert vector.angle_with(object()) is NotImplemented

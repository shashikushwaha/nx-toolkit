import math
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from nxopenkit.maths.vector3d import Vector3d


class TestVector3d(unittest.TestCase):
    def setUp(self):
        self.vector = Vector3d(1, 2, 3)
        self.other = Vector3d(4, 5, 6)

    def test_repr(self):
        self.assertEqual(repr(self.vector), "Vector3d(1, 2, 3)")

    def test_to_nx(self):
        with patch("nxopenkit.maths.vector3d.NXOpen") as nxopen:
            nx_vector = self.vector.to_nx
        self.assertIs(nx_vector, nxopen.Vector3d.return_value)
        nxopen.Vector3d.assert_called_once_with(1, 2, 3)

    def test_equality(self):
        self.assertEqual(self.vector, Vector3d(1, 2, 3))
        self.assertNotEqual(self.vector, self.other)
        self.assertIs(self.vector.__eq__(object()), NotImplemented)

    def test_addition(self):
        self.assertEqual(self.vector + self.other, Vector3d(5, 7, 9))
        self.assertIs(self.vector.__add__(object()), NotImplemented)

    def test_subtraction(self):
        self.assertEqual(self.vector - self.other, Vector3d(-3, -3, -3))
        self.assertIs(self.vector.__sub__(object()), NotImplemented)

    def test_multiplication(self):
        self.assertEqual(self.vector * 2, Vector3d(2, 4, 6))
        self.assertEqual(self.vector * 0.5, Vector3d(0.5, 1, 1.5))
        self.assertIs(self.vector.__mul__("2"), NotImplemented)

    def test_cross_product(self):
        self.assertEqual(self.vector.cross(self.other), Vector3d(-3, 6, -3))
        self.assertIs(self.vector.cross(object()), NotImplemented)

    def test_dot_product(self):
        self.assertEqual(self.vector.dot(self.other), 32)
        self.assertIs(self.vector.dot(object()), NotImplemented)

    def test_magnitude(self):
        self.assertAlmostEqual(self.vector.magnitude(), math.sqrt(14))
        self.assertEqual(Vector3d(0, 0, 0).magnitude(), 0)

    def test_normalize(self):
        normalized = self.vector.normalize()
        self.assertAlmostEqual(normalized.magnitude(), 1)
        with self.assertRaisesRegex(ValueError, "Cannot normalize the zero vector"):
            Vector3d(0, 0, 0).normalize()

    def test_angle_with(self):
        self.assertAlmostEqual(
            Vector3d(1, 0, 0).angle_with(Vector3d(0, 1, 0)), math.pi / 2
        )
        with self.assertRaisesRegex(ValueError, "Cannot compute angle with the zero vector"):
            self.vector.angle_with(Vector3d(0, 0, 0))
        self.assertIs(self.vector.angle_with(object()), NotImplemented)


if __name__ == "__main__":
    unittest.main()
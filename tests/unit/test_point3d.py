from unittest.mock import patch

import pytest

from nxopenkit.maths.point3d import Point3d
from nxopenkit.maths.vector3d import Vector3d

class TestPoint3d:

    def test_point3d_initialization(self):
        point = Point3d(1, 2, 3)
        assert point.x == 1
        assert point.y == 2
        assert point.z == 3

    def test_point3d_equality(self):
        point1 = Point3d(1, 2, 3)
        point2 = Point3d(1, 2, 3)
        point3 = Point3d(4, 5, 6)
        assert point1 == point2 
        assert point1 != point3

    def test_point3d_to_nx(self):
        point = Point3d(1, 2, 3)
        with patch("nxopenkit.maths.point3d.NXOpen") as nxopen:
            nx_point = point.to_nx
        assert nx_point is nxopen.Point3d.return_value
        nxopen.Point3d.assert_called_once_with(1, 2, 3)

    def test_point3d_addition(self):
        point = Point3d(1, 2, 3)
        vector = Point3d(4, 5, 6)
        result = point + vector
        assert result == Point3d(5, 7, 9)

    def test_point3d_subtraction(self):
        point1 = Point3d(4, 5, 6)
        point2 = Point3d(1, 2, 3)
        result = point1 - point2
        assert result == Point3d(3, 3, 3)

    def test_point3d_multiplication(self):
        point = Point3d(1, 2, 3)
        result = point * 2
        assert result == Point3d(2, 4, 6)

    def test_point3d_division(self):
        point = Point3d(4, 6, 8)
        result = point / 2
        assert result == Point3d(2, 3, 4)

    def test_distance_to(self):
        point1 = Point3d(1, 2, 3)
        point2 = Point3d(4, 5, 6)
        distance = point1.distance_to(point2)
        assert distance == pytest.approx(5.196152422706632) 

    def test_midpoint(self):
        point1 = Point3d(1, 2, 3)
        point2 = Point3d(4, 5, 6)
        midpoint = point1.midpoint(point2)
        assert midpoint == Point3d(2.5, 3.5, 4.5)

    def test_to_vector(self):
        point = Point3d(1, 2, 3)
        vector = point.to_vector()
        assert vector == Vector3d(1, 2, 3)

    def test_translation(self):
        point = Point3d(1, 2, 3)
        vector = Vector3d(4, 5, 6)
        translated_point = point.translate(vector)
        assert translated_point == Point3d(5, 7, 9) 

    def test_equals_with_rounding(self):
        point1 = Point3d(1.123456789, 2.123456789, 3.123456789)
        point2 = Point3d(1.123456780, 2.123456780, 3.123456780)
        assert point1.equals(point2, round_digit=8) is True
        assert point1.equals(point2, round_digit=9) is False

    def test_equals_with_non_point3d(self):
        point = Point3d(1, 2, 3)
        assert point.equals("not a Point3d") is NotImplemented

    def test_is_origin(self):
        point1 = Point3d(0, 0, 0)
        point2 = Point3d(1, 2, 3)
        assert point1.is_origin() is True
        assert point2.is_origin() is False
    def test_to_list(self):
        point = Point3d(1, 2, 3)
        assert point.to_list() == [1, 2, 3]

    def test_to_tuple(self):
        point = Point3d(1, 2, 3)
        assert point.to_tuple() == (1, 2, 3)

    def test_scale(self):
        point = Point3d(1, 2, 3)
        scaled_point = point.scale(2)
        assert scaled_point == Point3d(2, 4, 6)

    

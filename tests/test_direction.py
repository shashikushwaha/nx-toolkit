import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from nxopenkit.core.direction import Direction


class TestDirection(unittest.TestCase):
    def setUp(self):
        self.nx_direction = object()
        self.directions = Mock()
        self.work_part = Mock()
        self.work_part.to_nx.Directions = self.directions
        self.directions.CreateDirection.return_value = self.nx_direction
        work_part_patch = patch(
            "nxopenkit.core.direction.Part.work_part", return_value=self.work_part
        )
        work_part_patch.start()
        self.addCleanup(work_part_patch.stop)

    def assert_factory_result(self, factory, *arguments):
        result = factory(*arguments)
        self.assertIsInstance(result, Direction)
        self.assertIs(result.to_nx, self.nx_direction)
        self.directions.CreateDirection.assert_called_once_with(*arguments)

    def test_init_and_to_nx(self):
        direction = Direction(self.nx_direction)
        self.assertIs(direction.to_nx, self.nx_direction)

    def test_create_direction_from_vector(self):
        self.assert_factory_result(Direction.create_direction_from_vector, "origin", "vector", "update")

    def test_create_direction_from_line(self):
        self.assert_factory_result(Direction.create_direction_from_line, "line", "sense", "update")

    def test_create_direction_from_edge(self):
        self.assert_factory_result(Direction.create_direction_from_edge, "edge", "sense", "update")

    def test_create_direction_from_conic(self):
        self.assert_factory_result(Direction.create_direction_from_conic, "conic", "sense", "update")

    def test_create_direction_from_axis(self):
        self.assert_factory_result(Direction.create_direction_from_axis, "axis", "sense", "update")

    def test_create_direction_from_face_normal(self):
        self.assert_factory_result(Direction.create_direction_from_face_normal, "face", "sense", "update")

    def test_create_direction_from_plane_normal(self):
        self.assert_factory_result(Direction.create_direction_from_plane_normal, "plane", "sense", "update")

    def test_create_direction_from_sketch_normal(self):
        self.assert_factory_result(Direction.create_direction_from_sketch_normal, "sketch", "sense", "update")

    def test_create_direction_from_points(self):
        self.assert_factory_result(Direction.create_direction_from_points, "start", "end", "update")

    def test_create_direction_from_control_points(self):
        self.assert_factory_result(Direction.create_direction_from_control_points, "start", "end", "update")

    def test_create_direction_from_curve_parameter(self):
        self.assert_factory_result(
            Direction.create_direction_from_curve_parameter,
            "curve",
            "parameter",
            "option",
            "sense",
            "update",
        )

    def test_create_direction_from_curve_point(self):
        self.assert_factory_result(
            Direction.create_direction_from_curve_point,
            "curve",
            "point",
            "option",
            "sense",
            "update",
        )

    def test_create_direction_from_transform(self):
        self.assert_factory_result(Direction.create_direction_from_transform, "direction", "transform", "update")

    def test_create_direction_from_combine(self):
        self.assert_factory_result(Direction.create_direction_from_combine, "direction1", "direction2", "update")


if __name__ == "__main__":
    unittest.main()
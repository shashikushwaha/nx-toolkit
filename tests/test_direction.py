import os
import sys
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
try:
    import NXOpen  # noqa: F401
except Exception as exc:  # pragma: no cover
    pytest.skip(f"NXOpen unavailable or incompatible in this environment: {exc}", allow_module_level=True)

from nxopenkit.core.direction import Direction


@pytest.fixture
def direction_mocks():
    nx_direction = object()
    directions = Mock()
    work_part = Mock()
    work_part.to_nx.Directions = directions
    directions.CreateDirection.return_value = nx_direction
    with patch("nxopenkit.core.direction.Part.work_part", return_value=work_part):
        yield nx_direction, directions


def assert_factory_result(factory, directions, nx_direction, *arguments):
    result = factory(*arguments)
    assert isinstance(result, Direction)
    assert result.to_nx is nx_direction
    directions.CreateDirection.assert_called_once_with(*arguments)


class TestDirection:
    def test_init_and_to_nx(self, direction_mocks):
        nx_direction, _ = direction_mocks
        direction = Direction(nx_direction)
        assert direction.to_nx is nx_direction

    def test_create_direction_from_vector(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_vector, directions, nx_direction, "origin", "vector", "update")

    def test_create_direction_from_line(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_line, directions, nx_direction, "line", "sense", "update")

    def test_create_direction_from_edge(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_edge, directions, nx_direction, "edge", "sense", "update")

    def test_create_direction_from_conic(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_conic, directions, nx_direction, "conic", "sense", "update")

    def test_create_direction_from_axis(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_axis, directions, nx_direction, "axis", "sense", "update")

    def test_create_direction_from_face_normal(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_face_normal, directions, nx_direction, "face", "sense", "update")

    def test_create_direction_from_plane_normal(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_plane_normal, directions, nx_direction, "plane", "sense", "update")

    def test_create_direction_from_sketch_normal(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_sketch_normal, directions, nx_direction, "sketch", "sense", "update")

    def test_create_direction_from_points(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_points, directions, nx_direction, "start", "end", "update")

    def test_create_direction_from_control_points(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_control_points, directions, nx_direction, "start", "end", "update")

    def test_create_direction_from_curve_parameter(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(
            Direction.create_direction_from_curve_parameter,
            directions,
            nx_direction,
            "curve",
            "parameter",
            "option",
            "sense",
            "update",
        )

    def test_create_direction_from_curve_point(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(
            Direction.create_direction_from_curve_point,
            directions,
            nx_direction,
            "curve",
            "point",
            "option",
            "sense",
            "update",
        )

    def test_create_direction_from_transform(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_transform, directions, nx_direction, "direction", "transform", "update")

    def test_create_direction_from_combine(self, direction_mocks):
        nx_direction, directions = direction_mocks
        assert_factory_result(Direction.create_direction_from_combine, directions, nx_direction, "direction1", "direction2", "update")

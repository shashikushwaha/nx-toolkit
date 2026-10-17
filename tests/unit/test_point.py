import pytest
import NXOpen 

from nxopenkit.core.part import Part
from nxopenkit.core.point import Point
from nxopenkit.core.types import PointOnCurveLocationOption
from nxopenkit.maths.point3d import Point3d


@pytest.fixture
def test_fixture(project_root):
    file_path = str(project_root / "test-cases" / "curve.prt")
    part = Part.open_part(file_path)
    try:
        yield part
    finally:
        Part.close_all()


class TestPoint:
    def test_fixture_object(self, test_fixture):
        assert test_fixture.to_nx is not None

    @pytest.mark.parametrize(
            "percentage, help_point, result", 
            [
                (10, Point3d(0, -80, 100.2242), Point3d(0.0, -50.774, 100.2242)),
                (85, Point3d(0, -80, 100.2242), Point3d(0.0, 132.0858, 163.5903)),
                (20, Point3d(0.0, 154.2293, 201.4257), Point3d(0.0, 124.7046, 150.9786)),
                (80, Point3d(0.0, 154.2293, 201.4257), Point3d(0.0, -21.5480, 100.2243))
            ]
        )
    def test_create_point_on_curve_percentage(self, test_fixture, percentage, result, help_point):
        all_curves = [Part.get_curves("COMPOSITE_CURVE_01")[0], Part.get_curves("COMPOSITE_CURVE_02")[0]]
        actual = Point.create_point_on_Edge_Curve(all_curves, percentage,  help_point = help_point)
        assert actual.coordinates.equals(result, 4), (
            f"percentage={percentage}\n"
            f"expected={result}\n"
            f"actual={actual.coordinates}"
        )

    @pytest.mark.parametrize(
            "percentage, help_point, location, result", 
            [
                (10, Point3d(0, -80, 100.2242), PointOnCurveLocationOption.PercentParameter, Point3d(0.0, -50.774, 100.2242)),
                (85, Point3d(0, -80, 100.2242), PointOnCurveLocationOption.PercentParameter, Point3d(0.0, 132.0858, 163.5903)),
                (20, Point3d(0.0, 154.2293, 201.4257),PointOnCurveLocationOption.PercentParameter, Point3d(0.0, 124.7046, 150.9786)),
                (80, Point3d(0.0, 154.2293, 201.4257), PointOnCurveLocationOption.PercentParameter, Point3d(0.0, -21.5480, 100.2243)),
                (10, Point3d(0, -80, 100.2242), PointOnCurveLocationOption.PercentArcLength, Point3d(0.0, -50.774, 100.2242)),
                (85, Point3d(0, -80, 100.2242), PointOnCurveLocationOption.PercentArcLength, Point3d(0.0, 132.0858, 163.5903)),
                (20, Point3d(0.0, 154.2293, 201.4257),PointOnCurveLocationOption.PercentArcLength, Point3d(0.0, 124.7046, 150.9786)),
                (80, Point3d(0.0, 154.2293, 201.4257), PointOnCurveLocationOption.PercentArcLength, Point3d(0.0, -21.5480, 100.2243)),
                (45.12, Point3d(0, -80, 100.2242), PointOnCurveLocationOption.ArcLength, Point3d(0.0, -34.8800, 100.2243)),
                (248.23, Point3d(0, -80, 100.2242), PointOnCurveLocationOption.ArcLength, Point3d(0.0, 131.9893, 163.4257)),
            ]
        )
    def test_create_point_on_curve_percentage(self, test_fixture, percentage, result, location, help_point):
        all_curves = [Part.get_curves("COMPOSITE_CURVE_01")[0], Part.get_curves("COMPOSITE_CURVE_02")[0]]
        actual = Point.create_point_on_Edge_Curve(all_curves, percentage, location_option=location, help_point = help_point)
        assert actual.coordinates.equals(result, 4), (
            f"percentage={percentage}\n"
            f"expected={result}\n"
            f"actual={actual.coordinates}"
        )

    def test_create_point_on_face(self, test_fixture):
        face = Part.get_faces("FACE_01")[0]
        actual = Point.create_point_on_face(face, 0.60, 0.70)
        assert actual.coordinates.equals(Point3d(0.0, 58.2842, 220.0897), 4)

    def test_create_point_between_points(self, test_fixture):
        point1 = Point.create_point(Point3d(10,10,10))
        point2 = Point.create_point(Point3d(100,100,100))
        actual = Point.create_point_between_points(point1, point2, 60)
        assert actual.coordinates.equals(Point3d(0.0, 58.2842, 220.0897), 4)


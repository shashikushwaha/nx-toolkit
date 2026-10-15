import pytest
import NXOpen 

from nxopenkit.core.part import Part
from nxopenkit.core.point import Point
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

    def test_create_point_on_curve(self, test_fixture):
        all_curves = [Part.get_curves("COMPOSITE_CURVE_01")[0], Part.get_curves("COMPOSITE_CURVE_02")[0]]
        point_on_curve = Point.create_point_on_Edge_Curve(all_curves, 10, help_point= Point3d(0, -80, 100.2242))
        Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")
        assert isinstance(point_on_curve.to_nx, NXOpen.Point)
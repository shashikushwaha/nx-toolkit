import pytest
import NXOpen 

from nxopenkit.core.part import Part
from nxopenkit.core.curve import Curve


@pytest.fixture
def test_fixture(project_root):
    file_path = str(project_root / "test-cases" / "curve.prt")
    part = Part.open_part(file_path)
    try:
        yield part
    finally:
        Part.close_all()


class TestCurve:
    def test_named_object(self, test_fixture):
        assert test_fixture.to_nx is not None

    def test_compositive_curve(self, test_fixture):
        all_curves = Part.get_curves()
        comp_curve = Curve.create_composite_curve(all_curves)
        assert isinstance(comp_curve.to_nx, NXOpen.Curve)
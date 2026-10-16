import pytest
import NXOpen 

from nxopenkit.core.part import Part
from nxopenkit.core.measurement import Measurement


@pytest.fixture
def test_fixture(project_root):
    file_path = str(project_root / "test-cases" / "measurement.prt")
    part = Part.open_part(file_path)
    try:
        yield part
    finally:
        Part.close_all()


class TestMeasurement:
    def test_fixture_object(self, test_fixture):
        assert test_fixture.to_nx is not None

    def test_minimum_distane(self, test_fixture):
        # point_feat = Part.get_features("POINT_SET_01")[0]
        # points = point_feat.get_points;
        source_point = Part.get_points("SOURCE_POINT")[0]
        destination_point = Part.get_points("POINT_015")[0]        
        result = Measurement.get_minimum_dist(source_point, destination_point)
        assert  round(result.distance, 4) == 429.0178
from typing import cast

import pytest
import NXOpen 

from nxopenkit.core.displayable_object import DisplayableObject
from nxopenkit.core.part import Part
from nxopenkit.core.measurement import Measurement
from nxopenkit.core.point import Point
from nxopenkit.maths.point3d import Point3d


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
        source_point = Part.get_points("SOURCE_POINT")[0]
        destination_point = Part.get_points("POINT_015")[0]        
        result = Measurement.get_minimum_dist(source_point, destination_point)
        assert  round(result.distance, 4) == 429.0178

    def test_minimum_distane_point_point3d(self, test_fixture):
        source_point = Part.get_points("SOURCE_POINT")[0]  
        result = Measurement.get_minimum_dist(source_point, Point3d(0,0,0))
        assert  round(result.distance, 4) == 60.6246

    def test_minimum_distane_point3d(self, test_fixture):
        source_point = Point3d(0,0,0)
        destination_point = Part.get_points("POINT_015")[0]        
        result = Measurement.get_minimum_dist(source_point, destination_point)
        assert  round(result.distance, 4) == 423.3029

    def test_closet_object_point_points(self, test_fixture):
        point_feat = Part.get_features("POINT_SET_01")[0]
        points = point_feat.get_points;
        source_point = Part.get_points("SOURCE_POINT")[0]   
        result = Measurement.get_closest_object(source_point, points)
        assert  round(result.distance, 4) == 60.7168
        assert cast(Point, result.source_object).name == "SOURCE_POINT"
        assert cast(Point, result.destination_object).name == "POINT_014"

    def test_closet_object_curve_edges(self, test_fixture):
        body = Part.get_bodies("BODY_01")[0]
        edges = body.get_edges;
        source_curve = Part.get_curves("CURVE_01")[0]   
        result = Measurement.get_closest_object(source_curve, edges)
        assert  round(result.distance, 4) == 0.4656
        assert cast(DisplayableObject, result.destination_object).name == "EDGE_010"
        assert result.point_on_source.equals(Point3d(-51.7827,0.33167,99.67319), 4)
        assert result.point_on_destination.equals(Point3d(-51.7827,0.0,100.0), 4)

    def test_closet_object_point3d_Body(self, test_fixture):
        body = Part.get_bodies("BODY_01")   
        result = Measurement.get_closest_object(Point3d(0,0,0), body)
        assert  round(result.distance, 4) == 100.00
        assert result.point_on_source.equals(Point3d(0,0,0), 4)
        assert result.point_on_destination.equals(Point3d(0.0,0.0,100.0), 4)
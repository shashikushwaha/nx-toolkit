from pathlib import Path
from typing import Callable, List

import pytest
import NXOpen
import NXOpen.GeometricUtilities
import NXOpen.Features
from nxopenkit.core.direction import Direction
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.point import Point
from nxopenkit.core.types import BooleanType, SphereType
from nxopenkit.maths.point3d import Point3d
from nxopenkit.maths.vector3d import Vector3d
from nxopenkit.core.part import Part
from nxopenkit.core.feature import Feature
from nxopenkit.features.sphere import Sphere


@pytest.fixture
def setup(project_root: Path):
    file_path = str(project_root / "test-cases" / "block.prt")
    Part.open_part(file_path)
    center_point = Point.create_point(Point3d(50, 50, 0))
    yield  (SphereType.CenterPointAndDiameter, center_point, 25)
    Part.close_all()

@pytest.fixture
def builder_factory(setup):
    type1, origin_point1, diameter1  = setup

    def _make_builder(
            spr_type = SphereType.CenterPointAndDiameter,
            center_point = None,
            diameter = None,
            arc = None,
    ):
        return Sphere(
            spr_type or type1, 
            center_point or origin_point1,
            diameter or diameter1,
            arc,
            )    
    return _make_builder


class TestSphere:

    def test_reject_center_point_none(self):
        with pytest.raises(ValueError, match="center point is required for type CenterPointAndDiameter"):
            Sphere(SphereType.CenterPointAndDiameter, center_point= None)

    # def test_reject_diatmeter_none(self, setup):
    #     origin_point = Point.create_point(Point3d(0, 0, 0))
    #     with pytest.raises(ValueError, match="diameter is required for type AxisDiameterAndHeight"):
    #         Cylinder(CylinderType.AxisDiameterAndHeight, 100, origin_point, Vector3d(0,0,1), None)

    def test_reject_arc_none(self):
        with pytest.raises(ValueError, match="arc is required for type Arc"):
            Sphere(SphereType.Arc, arc = None)

    def test_sphere_by_center_point_diameter(self, builder_factory: Callable[..., Sphere]):
        builder = builder_factory()
        feature = builder.commit_feature()
        Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")
        assert isinstance(feature.to_nx, NXOpen.Features.Sphere)

    def test_sphere_by_arc(self, builder_factory: Callable[..., Sphere]):
        arc = Part.get_curves("ARC_01")[0]
        builder = builder_factory(SphereType.Arc, arc = arc)
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Sphere)

    def test_cylinder_and_commit(self, builder_factory: Callable[..., Sphere]):
        builder = builder_factory()
        committed_objects = builder.commit()
        assert isinstance(committed_objects[0], NXOpen.Features.Sphere)

    def test_boolean(self, builder_factory: Callable[..., Sphere]):
            bodies = Part.get_bodies("BODY_01")
            builder = builder_factory(diameter = 500)        
            result = builder.boolean(BooleanType.Unite, bodies)
            assert builder.nx_builder.BooleanOption.Type == BooleanType.Unite
            assert result is builder
            feature = builder.commit_feature()
            assert isinstance(feature.to_nx, NXOpen.Features.Sphere)
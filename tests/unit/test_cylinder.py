from pathlib import Path
from typing import Callable, List

import pytest
import NXOpen
import NXOpen.GeometricUtilities
import NXOpen.Features
from nxopenkit.core.direction import Direction
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.point import Point
from nxopenkit.core.types import BooleanType, CylinderType
from nxopenkit.maths.point3d import Point3d
from nxopenkit.maths.vector3d import Vector3d
from nxopenkit.core.part import Part
from nxopenkit.core.feature import Feature
from nxopenkit.features.cylinder import Cylinder


@pytest.fixture
def setup(project_root: Path):
    file_path = str(project_root / "test-cases" / "block.prt")
    Part.open_part(file_path)
    origin_point = Point.create_point(Point3d(0, 0, 0))
    vector =  Vector3d(0,0,1)
    yield  (CylinderType.AxisDiameterAndHeight, 100, origin_point, vector, 25)
    Part.close_all()

@pytest.fixture
def builder_factory(setup):
    type1, height, origin_point1, vector1, diameter1  = setup

    def _make_builder(
            cly_type = CylinderType.AxisDiameterAndHeight,
            origin_point = None,
            vector =  None,
            diameter = None,
            arc = None,
    ):
        return Cylinder(
            cly_type or type1, 
            height,
            origin_point or origin_point1, 
            vector or vector1,
            diameter or diameter1,
            arc,
            )    
    return _make_builder


class TestCylinder:
    def test_reject_height_none(self):
        with pytest.raises(ValueError, match="height is required for type AxisDiameterAndHeight"):
            Cylinder(CylinderType.AxisDiameterAndHeight, height=None)

    def test_reject_origin_point_none(self):
        with pytest.raises(ValueError, match="origin_point is required for type AxisDiameterAndHeight"):
            Cylinder(CylinderType.AxisDiameterAndHeight, 100, origin_point= None)

    def test_reject_vector_none(self, setup):
        origin_point = Point.create_point(Point3d(0, 0, 0))
        with pytest.raises(ValueError, match="vector is required for type AxisDiameterAndHeight"):
            Cylinder(CylinderType.AxisDiameterAndHeight, 100, origin_point, None)

    def test_reject_diatmeter_none(self, setup):
        origin_point = Point.create_point(Point3d(0, 0, 0))
        with pytest.raises(ValueError, match="diameter is required for type AxisDiameterAndHeight"):
            Cylinder(CylinderType.AxisDiameterAndHeight, 100, origin_point, Vector3d(0,0,1), None)

    def test_reject_arc_none(self, setup):
        with pytest.raises(ValueError, match="arc is required for type ArcAndHeight"):
            Cylinder(CylinderType.ArcAndHeight, 100, arc = None)

    def test_cylinder_and_commit_feature(self, builder_factory: Callable[..., Cylinder]):
        builder = builder_factory()
        feature = builder.commit_feature()
        Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")
        assert isinstance(feature.to_nx, NXOpen.Features.Cylinder)

    def test_arc_diameter(self, builder_factory: Callable[..., Cylinder]):
        arc = Part.get_curves("ARC_01")[0]
        builder = builder_factory(CylinderType.ArcAndHeight, arc = arc)
        feature = builder.commit_feature()
        Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")
        assert isinstance(feature.to_nx, NXOpen.Features.Cylinder)

    def test_cylinder_and_commit(self, builder_factory: Callable[..., Cylinder]):
        builder = builder_factory()
        committed_objects = builder.commit()
        assert isinstance(committed_objects[0], NXOpen.Features.Cylinder)

    def test_reject_nx_exception_boolean(self, builder_factory: Callable[..., Cylinder]):
        bodies = Part.get_bodies("BODY_01")
        builder = builder_factory()        
        result = builder.boolean(BooleanType.Unite, bodies)
        assert builder.nx_builder.BooleanOption.Type == BooleanType.Unite
        assert result is builder
        with pytest.raises(ValueError, match="Tool body completely outside target body."):
            builder.commit_feature()

    def test_boolean(self, builder_factory: Callable[..., Cylinder]):
            bodies = Part.get_bodies("BODY_01")
            builder = builder_factory(diameter = 500)        
            result = builder.boolean(BooleanType.Unite, bodies)
            assert builder.nx_builder.BooleanOption.Type == BooleanType.Unite
            assert result is builder
            feature = builder.commit_feature()
            assert isinstance(feature.to_nx, NXOpen.Features.Cylinder)
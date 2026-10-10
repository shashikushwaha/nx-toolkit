from pathlib import Path
from typing import Callable, List

import pytest
import NXOpen
import NXOpen.GeometricUtilities
import NXOpen.Features

from nxopenkit.core.direction import Direction
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.point import Point
from nxopenkit.maths.point3d import Point3d
from nxopenkit.maths.vector3d import Vector3d
from nxopenkit.modeling.revolve_builder import RevolveBuilder
from nxopenkit.core.part import Part
from nxopenkit.core.feature import Feature


@pytest.fixture
def setup(project_root: Path):
    file_path = str(project_root / "test-cases" / "face.prt")
    Part.open_part(file_path)
    edges = Part.get_edges("EDGE_08")
    axis_point = Point.create_point(Point3d(100, 100, 0))
    yield (edges, axis_point)
    Part.close_all()

@pytest.fixture
def revolve_builder_factory(setup):
    edges, axis_point = setup
    def _make_builder(
            curves = None,
            direction = None,
            point = None,
            start_angle = 0,
            end_angle = 360
    ):
        return RevolveBuilder(
            curves or edges, 
            direction or Vector3d(0, 0, 1), 
            point or axis_point, 
            start_angle,
            end_angle,
            )    
    return _make_builder


class TestRevolveBuilder:
    def test_rejects_empty_profile_curves(self):
        with pytest.raises(ValueError, match="At least one profile curve"):
            RevolveBuilder([], Vector3d(0, 0, 1), [], "0", 360)

    def test_settings_update_distance_and_return_builder(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        builder = revolve_builder_factory()
        result = builder.settings(NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet, tolerance=0.0001)
        assert result is builder
        assert builder.nx_builder.FeatureOptions.BodyType == NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Revolve)

    def test_revolve_and_commit_feature(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        builder = revolve_builder_factory()
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Revolve)

    def test_reject_revolve_with_datum_axis(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        axis = Part.get_datum_axes("AXIS_01")
        with pytest.raises(TypeError, match="direction must be DatumAxis, Direction, or Vector3d"):
            revolve_builder_factory(direction = axis)
        # Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")

    def test_revolve_with_datum_axis(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        axis = Part.get_datum_axes("AXIS_01")[0]
        builder = revolve_builder_factory(direction=axis)
        feature = builder.commit_feature()        
        parent = feature.to_nx.GetParents()
        # Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")
        assert isinstance(feature.to_nx, NXOpen.Features.Revolve)
        assert any(isinstance(f, NXOpen.Features.DatumAxisFeature) for f in parent)
    
    def test_revolve_with_direction(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        axis = Direction.create_direction_from_vector(Point3d(0,0,0), Vector3d(0,0,1))
        builder = revolve_builder_factory(direction=axis)
        feature = builder.commit_feature()        
        # Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")
        assert isinstance(feature.to_nx, NXOpen.Features.Revolve)

    def test_revolve_and_commit(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        builder = revolve_builder_factory()
        committed_objects = builder.commit()
        assert isinstance(committed_objects[0], NXOpen.Features.Revolve)

    def test_boolean_and_commit_feature(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        builder = revolve_builder_factory()
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Revolve)

    def test_offset(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        builder = revolve_builder_factory()
        result = builder.offset(
            NXOpen.GeometricUtilities.Type.NonsymmetricOffset,
            "-5", 5)
        assert result is builder
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Revolve)

    def test_boolean(self, revolve_builder_factory: Callable[..., RevolveBuilder]):
        bodies = Part.get_bodies("BODY_01")
        builder = revolve_builder_factory()        
        result = builder.boolean(
            NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Unite,
            bodies)
        assert builder.nx_builder.BooleanOperation.Type == NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Unite
        assert result is builder
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Revolve)

         
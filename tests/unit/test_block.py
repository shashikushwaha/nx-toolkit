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
from nxopenkit.modeling.block import Block
from nxopenkit.core.part import Part
from nxopenkit.core.feature import Feature


@pytest.fixture
def setup(project_root: Path):
    file_path = str(project_root / "test-cases" / "block.prt")
    Part.open_part(file_path)
    origin_point = Point.create_point(Point3d(0, 0, 0))
    first_point = Point.create_point(Point3d(100, 0, 0))
    second_point = Point.create_point(Point3d(100, 100, 0))
    yield (origin_point, first_point, second_point)
    Part.close_all()

@pytest.fixture
def block_builder_factory(setup):
    origin_point, first_point, second_point = setup
    xc_length = 100
    def _make_builder(
            type = NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths,
            origin_point1 = None,
            second_point1 = None,
            xc_length1 =  None,
            yc_length1 = None,
            zc_length1 = None,
    ):
        return Block(
            type, 
            origin_point or origin_point1, 
            second_point or second_point1,
            xc_length1 or xc_length,
            yc_length1 or xc_length,
            zc_length1 or xc_length,
            )    
    return _make_builder


class TestBlock:
    def test_rejects_empty_profile_curves(self):
        with pytest.raises(ValueError, match="At least one profile curve"):
            Block([])


    def test_revolve_and_commit_feature(self, block_builder_factory: Callable[..., Block]):
        builder = block_builder_factory()
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Block)

    def test_revolve_and_commit(self, block_builder_factory: Callable[..., Block]):
        builder = block_builder_factory()
        committed_objects = builder.commit()
        assert isinstance(committed_objects[0], NXOpen.Features.Block)

    def test_boolean_and_commit_feature(self, block_builder_factory: Callable[..., Block]):
        builder = block_builder_factory()
        feature = builder.commit_feature()
        Part.save_as(r"C:\D\Shashi\nx-toolkit\test-cases\temp\test.prt")
        assert isinstance(feature.to_nx, NXOpen.Features.Block)

    def test_boolean(self, block_builder_factory: Callable[..., Block]):
        bodies = Part.get_bodies("BODY_01")
        builder = block_builder_factory()        
        result = builder.boolean(
            NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Unite,
            bodies)
        assert builder.nx_builder.BooleanOperation.Type == NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Unite
        assert result is builder
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Block)

         
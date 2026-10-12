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
    origin_point1, first_point, second_point1 = setup
    xc_length = 100
    def _make_builder(
            type = NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths,
            origin_point = None,
            second_point = None,
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
    def test_reject_origin_point_none(self):
            with pytest.raises(TypeError, match="origin_point"):
                Block(NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths, None)


    def test_block_and_commit_feature(self, block_builder_factory: Callable[..., Block]):
        builder = block_builder_factory()
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Block)

    def test_block_and_commit(self, block_builder_factory: Callable[..., Block]):
        builder = block_builder_factory()
        committed_objects = builder.commit()
        assert isinstance(committed_objects[0], NXOpen.Features.Block)

    # @pytest.mark.parametrize("type", [NXOpen.Features.BlockFeatureBuilder.Types.TwoPointsAndHeight, NXOpen.Features.BlockFeatureBuilder.Types.DiagonalPoints])
    def test_block_by_two_points_and_height(self, block_builder_factory: Callable[..., Block]):
        builder = block_builder_factory(type = NXOpen.Features.BlockFeatureBuilder.Types.TwoPointsAndHeight)
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Block)

    def test_block_by_diagonal_point(self, block_builder_factory: Callable[..., Block]):
        second_point = Point.create_point(Point3d(100, 100, 100))
        builder = block_builder_factory(type = NXOpen.Features.BlockFeatureBuilder.Types.DiagonalPoints, second_point = second_point)
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Block)

    def test_boolean(self, block_builder_factory: Callable[..., Block]):
        bodies = Part.get_bodies("BODY_01")[0]
        builder = block_builder_factory()        
        result = builder.boolean(NXOpen.Features.Feature.BooleanType.Unite, bodies)
        assert builder.nx_builder.BooleanType == NXOpen.Features.Feature.BooleanType.Unite
        assert result is builder
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Block)

         
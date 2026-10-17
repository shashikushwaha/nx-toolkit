from pathlib import Path
from typing import Callable, List

import pytest
import NXOpen
import NXOpen.GeometricUtilities
import NXOpen.Features

from nxopenkit.core.edge import Edge
from nxopenkit.features.extrude import Extrude
from nxopenkit.core.part import Part
from nxopenkit.maths.vector3d import Vector3d


@pytest.fixture
def setup(project_root: Path):
    file_path = str(project_root / "test-cases" / "body.prt")
    Part.open_part(file_path)
    edges = Part.get_faces("FACE_016")[0].get_edges()
    yield edges
    Part.close_all()

@pytest.fixture
def extrude_factory(setup: List[Edge]):
    def _make_builder():
        return Extrude(setup, "0", 10, direction=Vector3d(0, 0, 1))    
    return _make_builder


class TestExtrude:
    def test_rejects_empty_profile_curves(self):
        with pytest.raises(ValueError, match="At least one profile curve"):
            Extrude([], 10.0)

    def test_settings_update_distance_and_return_builder(self, extrude_factory: Callable[[], Extrude]):
        builder = extrude_factory()
        result = builder.settings(NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet, tolerance=0.0001)
        assert result is builder
        assert builder.nx_builder.FeatureOptions.BodyType == NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Extrude)

    def test_extrude_and_commit_feature(self, extrude_factory: Callable[[], Extrude], project_root: Path):
        builder = extrude_factory()
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Extrude)

    def test_extrude_and_commit(self, extrude_factory: Callable[[], Extrude]):
        builder = extrude_factory()
        committed_objects = builder.commit()
        assert isinstance(committed_objects[0], NXOpen.Features.Extrude)

    def test_draft_and_commit_feature(self, extrude_factory: Callable[[], Extrude]):
        builder = extrude_factory()
        builder.draft(NXOpen.GeometricUtilities.SimpleDraft.SimpleDraftType.SimpleFromProfile, "3.0")        
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Extrude)

    def test_draft_with_angle_option(self, extrude_factory: Callable[[], Extrude]):
        builder = extrude_factory()
        builder.draft(NXOpen.GeometricUtilities.SimpleDraft.SimpleDraftType.SimpleFromProfile, "3", NXOpen.GeometricUtilities.MultiDraft.AngleOption.Multiple)
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Extrude)

    def test_boolean_and_commit_feature(self, extrude_factory: Callable[[], Extrude]):
        builder = extrude_factory()
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Extrude)

    def test_offset(self, extrude_factory: Callable[[], Extrude]):
        builder = extrude_factory()
        builder.offset(
            NXOpen.GeometricUtilities.Type.NonsymmetricOffset,
            "-5", 5)
        builder.draft(NXOpen.GeometricUtilities.SimpleDraft.SimpleDraftType.SimpleFromProfile, "3.0")
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Extrude)

    def test_boolean(self, extrude_factory: Callable[[], Extrude]):
        bodies = Part.get_bodies("BODY_02")
        builder = extrude_factory()        
        result = builder.boolean(
            NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Unite,
            bodies)
        assert builder.nx_builder.BooleanOperation.Type == NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Unite
        assert result is builder
        feature = builder.commit_feature()
        assert isinstance(feature.to_nx, NXOpen.Features.Extrude)
         
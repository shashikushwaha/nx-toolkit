import os
import sys

import pytest


try:
    import NXOpen
except Exception as exc:  # pragma: no cover
    pytest.skip(f"NXOpen unavailable or incompatible in this environment: {exc}", allow_module_level=True)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxopenkit.modeling.extrude_builder import ExtrudeBuilder
from nxopenkit.core.part import Part
from nxopenkit.maths.vector3d import Vector3d


@pytest.fixture
def extrude_builder_factory():
    def _make_builder():
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "test-cases", "body.prt")
        )
        Part.open_part(file_path)
        edges = Part.get_faces("FACE_016")[0].get_edges()
        return ExtrudeBuilder(edges, "0", 10, direction=Vector3d(0, 0, 1))

    yield _make_builder
    Part.close_all()


class TestExtrudeBuilder:
    def test_rejects_empty_profile_curves(self):
        with pytest.raises(ValueError, match="At least one profile curve"):
            ExtrudeBuilder([], 10.0)

    def test_settings_update_distance_and_return_builder(self, extrude_builder_factory):
        builder = extrude_builder_factory()
        result = builder.settings(NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet, tolerance=0.0001)
        assert result is builder
        assert builder.nx_builder.FeatureOptions.BodyType == NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet
        feature = builder.commit_feature()
        assert feature is not None

    def test_extrude_and_commit_feature(self, extrude_builder_factory):
        builder = extrude_builder_factory()
        feature = builder.commit_feature()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-cases", "temp", "test.prt"))
        Part.save_as(file_path)
        assert feature is not None

    def test_extrude_and_commit(self, extrude_builder_factory):
        builder = extrude_builder_factory()
        committed_objects = builder.commit()
        assert committed_objects

    def test_draft_and_commit_feature(self, extrude_builder_factory):
        builder = extrude_builder_factory()
        builder.draft(NXOpen.GeometricUtilities.SimpleDraft.SimpleDraftType., 2, Vector3d(0,0,1))
        feature = builder.commit_feature()
        assert feature is not None

    def test_boolean_and_commit_feature(self, extrude_builder_factory):
        builder = extrude_builder_factory()
        feature = builder.commit_feature()
        assert feature is not None


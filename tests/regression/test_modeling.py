from nxopenkit import ExtrudeBuilder, Part, Vector3d
import pytest

@pytest.fixture
def extrude_builder_factory(project_root):
    def _make_builder():
        file_path = str(project_root / "test-cases" / "body.prt")
        Part.open_part(file_path)
        edges = Part.get_faces("FACE_016")[0].get_edges()
        return ExtrudeBuilder(edges, "0", 10, direction=Vector3d(0, 0, 1))

    yield _make_builder
    Part.close_all()

class TestModelling:
    def test_extrude_and_commit(self, extrude_builder_factory):
        builder = extrude_builder_factory()
        committed_objects = builder.commit()
        assert committed_objects

    def test_boolean_and_commit_feature(self, extrude_builder_factory):
        builder = extrude_builder_factory()
        feature = builder.commit_feature()
        assert feature is not None
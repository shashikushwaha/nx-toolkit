

import pytest

# import importlib
# try:
#     importlib.import_module("NXOpen.UF")
# except Exception as exc:  # pragma: no cover
#     pytest.skip(f"NXOpen unavailable or incompatible in this environment: {exc}", allow_module_level=True)
# import NXOpen

from nxopenkit.core.part import Part


@pytest.fixture
def part_factory(project_root):
    def _open(fixture_name):
        file_path = str(project_root / "test-cases" / fixture_name)
        return Part.open_part(file_path)

    yield _open
    Part.close_all()


class TestPart:
    def test_get_bodies(self, part_factory):
        part_factory("body.prt")
        all_bodies = Part.get_bodies()
        assert len(all_bodies) == 3

    def test_get_faces(self, part_factory):
        part_factory("face.prt")
        all_faces = Part.get_faces()
        assert len(all_faces) == 6

    def test_get_edges(self, part_factory):
        part_factory("face.prt")
        all_edges = Part.get_edges()
        assert len(all_edges) == 12

    def test_get_displayable_objects(self, part_factory):
        part_factory("face.prt")
        all_displayables = Part.get_displayable_objects()
        assert len(all_displayables) == 29
        assert all(obj.to_nx is not None for obj in all_displayables)

    def test_get_part(self, part_factory):
        part = part_factory("part.prt")
        assert part.to_nx is not None

    def test_get_body_name(self, part_factory):
        part_factory("named-object.prt")
        body = Part.get_bodies("BODY_01")
        assert body is not None
        assert body[0].to_nx is not None

    def test_failed_get_body_name(self, part_factory):
        part_factory("named-object.prt")
        with pytest.raises(ValueError, match=r"BODY_011 not found\."):
            Part.get_bodies("BODY_011")

    def test_get_points(self, part_factory):
        part_factory("points.prt")
        all_points = Part.get_points()
        assert len(all_points) == 6

    def test_get_point_name(self, part_factory):
        part_factory("points.prt")
        point = Part.get_points("POINT_04")
        assert point is not None
        assert point[0].to_nx is not None

    def test_get_curve(self, part_factory):
        part_factory("part.prt")
        all_curves = Part.get_curves()
        assert len(all_curves) == 4

    def test_get_curve_name(self, part_factory):
        part_factory("part.prt")
        curve = Part.get_curves("CURVE_01")
        assert curve is not None
        assert curve[0].to_nx is not None

    def test_get_datum_plane(self, part_factory):
        part_factory("part.prt")
        datum_plane = Part.get_datum_planes()
        assert len(datum_plane) == 19
        assert datum_plane[0].to_nx is not None

    def test_get_csys(self, part_factory):
        part_factory("part.prt")
        datum_csys = Part.get_datum_csys()
        assert len(datum_csys) == 6
        assert datum_csys[0].to_nx is not None

    def test_get_csys_by_name(self, part_factory):
        part_factory("part.prt")
        datum_csys = Part.get_datum_csys("CSYS_01")
        assert datum_csys is not None
        assert datum_csys[0].to_nx is not None

    def test_get_datum_axis(self, part_factory):
        part_factory("part.prt")
        datum_axis = Part.get_datum_axes()
        assert len(datum_axis) == 18

    def test_datum_plane_name(self, part_factory):
        part_factory("part.prt")
        datum_plane = Part.get_datum_planes("DATUM_02")
        assert datum_plane is not None
        assert datum_plane[0].to_nx is not None

    def test_datum_axis_name(self, part_factory):
        part_factory("part.prt")
        datum_axis = Part.get_datum_axes("AXIS_01")
        assert datum_axis is not None
        assert datum_axis[0].to_nx is not None

    def test_failed_get_datum_plane_name(self, part_factory):
        part_factory("part.prt")
        with pytest.raises(ValueError, match=r"DATUM_PLANE_011 not found\."):
            Part.get_datum_planes("DATUM_PLANE_011")

    def test_failed_get_datum_axis_name(self, part_factory):
        part_factory("part.prt")
        with pytest.raises(ValueError, match=r"DATUM_AXIS_011 not found\."):
            Part.get_datum_axes("DATUM_AXIS_011")

    def test_failed_get_curve_name(self, part_factory):
        part_factory("part.prt")
        with pytest.raises(ValueError, match=r"CURVE_011 not found\."):
            Part.get_curves("CURVE_011")

    def test_failed_get_point_name(self, part_factory):
        part_factory("points.prt")
        with pytest.raises(ValueError, match=r"POINT_011 not found\."):
            Part.get_points("POINT_011")

    def test_failed_get_edge_name(self, part_factory):
        part_factory("face.prt")
        with pytest.raises(ValueError, match=r"EDGE_01111 not found\."):
            Part.get_edges("EDGE_01111")

    def test_failed_get_face_name(self, part_factory):
        part_factory("face.prt")
        with pytest.raises(ValueError, match=r"FACE_011 not found\."):
            Part.get_faces("FACE_011")

    def test_failed_get_displayable_object_name(self, part_factory):
        part_factory("part.prt")
        with pytest.raises(ValueError, match=r"DISPLAYABLE_011 not found\."):
            Part.get_displayable_objects("DISPLAYABLE_011")

    def test_get_displayable_object_name(self, part_factory):
        part_factory("face.prt")
        displayable = Part.get_displayable_objects("FACE_01")
        assert displayable[0] is not None
        assert displayable[0].to_nx is not None

    def test_get_displayable_object_name_body(self, part_factory):
        part_factory("named-object.prt")
        displayable = Part.get_displayable_objects("BODY_01")
        assert displayable[0] is not None
        assert displayable[0].to_nx is not None

    def test_get_displayable_object_name_point(self, part_factory):
        part_factory("points.prt")
        displayable = Part.get_displayable_objects("POINT_01")
        assert displayable[0] is not None
        assert displayable[0].to_nx is not None

    def test_get_feature(self, part_factory):
        part_factory("part.prt")
        all_features = Part.get_features()
        assert len(all_features) == 17

    def test_get_feature_name(self, part_factory):
        part_factory("part.prt")
        feature = Part.get_features("CUBE")
        assert feature[0] is not None
        assert feature[0].to_nx is not None

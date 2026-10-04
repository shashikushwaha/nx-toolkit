import os
import sys

import pytest

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(workspace_root, "src"))
pytestmark = pytest.mark.skipif(
    not os.environ.get("UGII_BASE_DIR"),
    reason="UFManager integration tests require UGII_BASE_DIR",
)

nx_root = os.environ.get("UGII_BASE_DIR")
if nx_root:
    sys.path.insert(0, os.path.join(nx_root, "NXBIN", "python"))
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(os.path.join(nx_root, "NXBIN"))

try:
    import NXOpen
except Exception as exc:  # pragma: no cover
    pytest.skip(f"NXOpen unavailable or incompatible in this environment: {exc}", allow_module_level=True)
from nxopenkit.core.part import Part
from nxopenkit.core.uf_manager import UFManager


@pytest.fixture
def uf_manager_context():
    part_path = os.path.join(workspace_root, "test-cases", "part.prt")
    Part.open_part(part_path)
    work_part = Part.work_part()
    try:
        yield work_part
    finally:
        Part.close_all()


def body_tag(work_part):
    bodies = list(work_part.bodies())
    assert bodies, "part.prt must contain a body"
    return bodies[0].tag


def face_tag(work_part):
    for body in work_part.bodies():
        faces = body.to_nx.GetFaces()
        if faces:
            return faces[0].Tag
    pytest.fail("part.prt must contain a face")


def edge_tag(work_part):
    for body in work_part.bodies():
        for face in body.to_nx.GetFaces():
            edges = face.GetEdges()
            if edges:
                return edges[0].Tag
    pytest.fail("part.prt must contain an edge")


def curve_tag(work_part):
    curves = list(work_part.Curves)
    assert curves, "part.prt must contain a curve"
    return curves[0].Tag


def create_test_line():
    line = NXOpen.UF.Curve.Line()
    line.StartPoint = [0.0, 0.0, 0.0]
    line.EndPoint = [1.0, 0.0, 0.0]
    return UFManager.create_line(line)


def create_test_arc():
    wcs_tag = UFManager.ask_work_coordinate_system()
    matrix_tag = UFManager.ask_matrix_of_object(wcs_tag)
    arc = NXOpen.UF.Curve.Arc()
    arc.ArcCenter = [0.0, 0.0, 0.0]
    arc.StartAngle = 0.0
    arc.EndAngle = 1.5707963267948966
    arc.Radius = 1.0
    arc.MatrixTag = matrix_tag
    return UFManager.create_arc(arc)


class TestUFManager:
    def test_ask_object_name(self, uf_manager_context):
        assert UFManager.ask_object_name(body_tag(uf_manager_context)) is not None

    def test_set_object_name(self, uf_manager_context):
        line_tag = create_test_line()
        try:
            UFManager.set_object_name(line_tag, "UF_MANAGER_TEST_LINE")
            assert UFManager.ask_object_name(line_tag) == "UF_MANAGER_TEST_LINE"
        finally:
            UFManager.delete_object(line_tag)

    def test_ask_object_type_and_subtype(self, uf_manager_context):
        object_type, object_subtype = UFManager.ask_object_type_and_subtype(body_tag(uf_manager_context))
        assert int(object_type) == 70
        assert int(object_subtype) == 0

    def test_ask_object_status(self, uf_manager_context):
        assert UFManager.ask_object_status(body_tag(uf_manager_context)) is not None

    def test_set_object_blank_status(self, uf_manager_context):
        line_tag = create_test_line()
        try:
            UFManager.set_object_blank_status(line_tag, NXOpen.UF.UFConstants.UF_OBJ_NOT_BLANKED)
            assert UFManager.ask_object_status(line_tag) is not None
        finally:
            UFManager.delete_object(line_tag)

    def test_delete_object(self, uf_manager_context):
        line_tag = create_test_line()
        UFManager.delete_object(line_tag)

    def test_ask_body_type(self, uf_manager_context):
        assert UFManager.ask_body_type(body_tag(uf_manager_context)) is not None

    def test_ask_body_faces(self, uf_manager_context):
        assert UFManager.ask_body_faces(body_tag(uf_manager_context)) is not None

    def test_ask_body_edges(self, uf_manager_context):
        assert UFManager.ask_body_edges(body_tag(uf_manager_context)) is not None

    def test_ask_face_edges(self, uf_manager_context):
        assert UFManager.ask_face_edges(face_tag(uf_manager_context)) is not None

    def test_ask_edge_vertices(self, uf_manager_context):
        assert UFManager.ask_edge_vertices(edge_tag(uf_manager_context)) is not None

    def test_ask_edge_faces(self, uf_manager_context):
        assert UFManager.ask_edge_faces(edge_tag(uf_manager_context)) is not None

    def test_ask_face_data(self, uf_manager_context):
        assert UFManager.ask_face_data(face_tag(uf_manager_context)) is not None

    def test_ask_face_body(self, uf_manager_context):
        assert UFManager.ask_face_body(face_tag(uf_manager_context)) == body_tag(uf_manager_context)

    def test_ask_edge_type(self, uf_manager_context):
        assert UFManager.ask_edge_type(edge_tag(uf_manager_context)) is not None

    def test_ask_face_type(self, uf_manager_context):
        assert UFManager.ask_face_type(face_tag(uf_manager_context)) is not None

    def test_ask_point_containment(self, uf_manager_context):
        point = [0.0, 0.0, 0.0]
        assert UFManager.ask_point_containment(point, body_tag(uf_manager_context)) is not None

    def test_ask_minimum_distance(self, uf_manager_context):
        result = UFManager.ask_minimum_distance(
            body_tag(uf_manager_context),
            face_tag(uf_manager_context),
            0,
            [0.0, 0.0, 0.0],
            0,
            [0.0, 0.0, 0.0],
        )
        assert result[0] >= 0.0

    def test_ask_bounding_box(self, uf_manager_context):
        assert UFManager.ask_bounding_box(body_tag(uf_manager_context)) is not None

    def test_ask_aligned_bounding_box(self, uf_manager_context):
        wcs_tag = UFManager.ask_work_coordinate_system()
        assert UFManager.ask_aligned_bounding_box(body_tag(uf_manager_context), wcs_tag, False) is not None

    def test_ask_exact_bounding_box(self, uf_manager_context):
        wcs_tag = UFManager.ask_work_coordinate_system()
        assert UFManager.ask_exact_bounding_box(body_tag(uf_manager_context), wcs_tag) is not None

    def test_ask_curve_closed(self, uf_manager_context):
        line_tag = create_test_line()
        try:
            assert UFManager.ask_curve_closed(line_tag) in (0, 1)
        finally:
            UFManager.delete_object(line_tag)

    def test_ask_curve_properties(self, uf_manager_context):
        line_tag = create_test_line()
        try:
            assert UFManager.ask_curve_properties(line_tag, 0.5) is not None
        finally:
            UFManager.delete_object(line_tag)

    def test_ask_line_data(self, uf_manager_context):
        line_tag = create_test_line()
        try:
            assert UFManager.ask_line_data(line_tag) is not None
        finally:
            UFManager.delete_object(line_tag)

    def test_ask_arc_data(self, uf_manager_context):
        arc_tag = create_test_arc()
        try:
            assert UFManager.ask_arc_data(arc_tag) is not None
        finally:
            UFManager.delete_object(arc_tag)

    def test_ask_point_data(self, uf_manager_context):
        point = uf_manager_context.to_nx.Points.CreatePoint(NXOpen.Point3d(0.0, 0.0, 0.0))
        try:
            assert UFManager.ask_point_data(point.Tag) is not None
        finally:
            UFManager.delete_object(point.Tag)

    def test_create_line(self, uf_manager_context):
        line_tag = create_test_line()
        assert line_tag is not None
        UFManager.delete_object(line_tag)

    def test_create_arc(self, uf_manager_context):
        arc_tag = create_test_arc()
        assert arc_tag is not None
        UFManager.delete_object(arc_tag)

    def test_ask_part_units(self, uf_manager_context):
        assert UFManager.ask_part_units(uf_manager_context.tag) is not None

    def test_ask_work_coordinate_system(self, uf_manager_context):
        assert UFManager.ask_work_coordinate_system() is not None

    def test_set_work_coordinate_system(self, uf_manager_context):
        wcs_tag = UFManager.ask_work_coordinate_system()
        UFManager.set_work_coordinate_system(wcs_tag)
        assert UFManager.ask_work_coordinate_system() == wcs_tag

    def test_ask_matrix_of_object(self, uf_manager_context):
        wcs_tag = UFManager.ask_work_coordinate_system()
        assert UFManager.ask_matrix_of_object(wcs_tag) is not None

    def test_open_listing_window(self, uf_manager_context):
        UFManager.open_listing_window()
        try:
            assert UFManager.is_listing_window_open() is True
        finally:
            UFManager.close_listing_window()

    def test_write_listing_window(self, uf_manager_context):
        UFManager.open_listing_window()
        try:
            UFManager.write_listing_window("pytest listing window test")
            assert UFManager.is_listing_window_open() is True
        finally:
            UFManager.close_listing_window()

    def test_close_listing_window(self, uf_manager_context):
        UFManager.open_listing_window()
        try:
            UFManager.close_listing_window()
            assert UFManager.is_listing_window_open() is False
        finally:
            UFManager.close_listing_window()

    def test_is_listing_window_open(self, uf_manager_context):
        UFManager.open_listing_window()
        try:
            assert UFManager.is_listing_window_open() is True
        finally:
            UFManager.close_listing_window()

    def test_ask_display_color(self, uf_manager_context):
        result = UFManager.ask_display_color(1, NXOpen.UF.UFConstants.UF_DISP_rgb_model)
        assert result is not None

    def test_set_display_color(self, uf_manager_context):
        color_model = NXOpen.UF.UFConstants.UF_DISP_rgb_model
        color_name, color_values = UFManager.ask_display_color(1, color_model)
        UFManager.set_display_color(1, color_model, color_name, color_values)

    def test_ask_work_view(self, uf_manager_context):
        assert UFManager.ask_work_view() is not None

    def test_fit_view(self, uf_manager_context):
        UFManager.fit_view(UFManager.ask_work_view(), 0.8)

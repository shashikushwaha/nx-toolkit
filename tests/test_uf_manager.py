import os
import sys
import unittest

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(workspace_root, "src"))
nx_root = os.environ.get("UGII_BASE_DIR")
if not nx_root:
	raise unittest.SkipTest("UFManager integration tests require UGII_BASE_DIR")

sys.path.insert(0, os.path.join(nx_root, "NXBIN", "python"))
if hasattr(os, "add_dll_directory"):
	_nx_dll_directory = os.add_dll_directory(os.path.join(nx_root, "NXBIN"))

import NXOpen
from nxopenkit.core.part import Part
from nxopenkit.core.uf_manager import UFManager


class TestUFManager(unittest.TestCase):
	def setUp(self):
		part_path = os.path.join(workspace_root, "test-cases", "part.prt")
		self.part = Part.open_part(part_path)
		self.work_part = Part.work_part()

	def tearDown(self):
		Part.close_all()

	def body_tag(self):
		bodies = list(self.work_part.bodies())
		self.assertTrue(bodies, "part.prt must contain a body")
		return bodies[0].tag

	def face_tag(self):
		for body in self.work_part.bodies():
			faces = body.to_nx.GetFaces()
			if faces:
				return faces[0].Tag
		self.fail("part.prt must contain a face")

	def edge_tag(self):
		for body in self.work_part.bodies():
			for face in body.to_nx.GetFaces():
				edges = face.GetEdges()
				if edges:
					return edges[0].Tag
		self.fail("part.prt must contain an edge")

	def curve_tag(self):
		curves = list(self.work_part.Curves)
		self.assertTrue(curves, "part.prt must contain a curve")
		return curves[0].Tag

	def create_test_line(self):
		line = NXOpen.UF.Curve.Line()
		line.StartPoint = [0.0, 0.0, 0.0]
		line.EndPoint = [1.0, 0.0, 0.0]
		return UFManager.create_line(line)

	def create_test_arc(self):
		wcs_tag = UFManager.ask_work_coordinate_system()
		matrix_tag = UFManager.ask_matrix_of_object(wcs_tag)
		arc = NXOpen.UF.Curve.Arc()
		arc.ArcCenter = [0.0, 0.0, 0.0]
		arc.StartAngle = 0.0
		arc.EndAngle = 1.5707963267948966
		arc.Radius = 1.0
		arc.MatrixTag = matrix_tag
		return UFManager.create_arc(arc)

	def test_ask_object_name(self):
		self.assertIsNotNone(UFManager.ask_object_name(self.body_tag()))

	def test_set_object_name(self):
		line_tag = self.create_test_line()
		try:
			UFManager.set_object_name(line_tag, "UF_MANAGER_TEST_LINE")
			self.assertEqual(UFManager.ask_object_name(line_tag), "UF_MANAGER_TEST_LINE")
		finally:
			UFManager.delete_object(line_tag)

	def test_ask_object_type_and_subtype(self):
		object_type, object_subtype = UFManager.ask_object_type_and_subtype(self.body_tag())
		self.assertEqual(int(object_type), 70)
		self.assertEqual(int(object_subtype), 0)

	def test_ask_object_status(self):
		self.assertIsNotNone(UFManager.ask_object_status(self.body_tag()))

	def test_set_object_blank_status(self):
		line_tag = self.create_test_line()
		try:
			UFManager.set_object_blank_status(line_tag, NXOpen.UF.UFConstants.UF_OBJ_NOT_BLANKED)
			self.assertIsNotNone(UFManager.ask_object_status(line_tag))
		finally:
			UFManager.delete_object(line_tag)

	def test_delete_object(self):
		line_tag = self.create_test_line()
		UFManager.delete_object(line_tag)

	def test_ask_body_type(self):
		self.assertIsNotNone(UFManager.ask_body_type(self.body_tag()))

	def test_ask_body_faces(self):
		self.assertIsNotNone(UFManager.ask_body_faces(self.body_tag()))

	def test_ask_body_edges(self):
		self.assertIsNotNone(UFManager.ask_body_edges(self.body_tag()))

	def test_ask_face_edges(self):
		self.assertIsNotNone(UFManager.ask_face_edges(self.face_tag()))

	def test_ask_edge_vertices(self):
		self.assertIsNotNone(UFManager.ask_edge_vertices(self.edge_tag()))

	def test_ask_edge_faces(self):
		self.assertIsNotNone(UFManager.ask_edge_faces(self.edge_tag()))

	def test_ask_face_data(self):
		self.assertIsNotNone(UFManager.ask_face_data(self.face_tag()))

	def test_ask_face_body(self):
		self.assertEqual(UFManager.ask_face_body(self.face_tag()), self.body_tag())

	def test_ask_edge_type(self):
		self.assertIsNotNone(UFManager.ask_edge_type(self.edge_tag()))

	def test_ask_face_type(self):
		self.assertIsNotNone(UFManager.ask_face_type(self.face_tag()))

	def test_ask_point_containment(self):
		point = [0.0, 0.0, 0.0]
		self.assertIsNotNone(UFManager.ask_point_containment(point, self.body_tag()))

	def test_ask_minimum_distance(self):
		result = UFManager.ask_minimum_distance(
			self.body_tag(), self.face_tag(), 0, [0.0, 0.0, 0.0], 0, [0.0, 0.0, 0.0]
		)
		self.assertGreaterEqual(result[0], 0.0)

	def test_ask_bounding_box(self):
		self.assertIsNotNone(UFManager.ask_bounding_box(self.body_tag()))

	def test_ask_aligned_bounding_box(self):
		wcs_tag = UFManager.ask_work_coordinate_system()
		self.assertIsNotNone(UFManager.ask_aligned_bounding_box(self.body_tag(), wcs_tag, False))

	def test_ask_exact_bounding_box(self):
		wcs_tag = UFManager.ask_work_coordinate_system()
		self.assertIsNotNone(UFManager.ask_exact_bounding_box(self.body_tag(), wcs_tag))

	def test_ask_curve_closed(self):
		line_tag = self.create_test_line()
		try:
			self.assertIn(UFManager.ask_curve_closed(line_tag), (0, 1))
		finally:
			UFManager.delete_object(line_tag)

	def test_ask_curve_properties(self):
		line_tag = self.create_test_line()
		try:
			self.assertIsNotNone(UFManager.ask_curve_properties(line_tag, 0.5))
		finally:
			UFManager.delete_object(line_tag)

	def test_ask_line_data(self):
		line_tag = self.create_test_line()
		try:
			self.assertIsNotNone(UFManager.ask_line_data(line_tag))
		finally:
			UFManager.delete_object(line_tag)

	def test_ask_arc_data(self):
		arc_tag = self.create_test_arc()
		try:
			self.assertIsNotNone(UFManager.ask_arc_data(arc_tag))
		finally:
			UFManager.delete_object(arc_tag)

	def test_ask_point_data(self):
		point = self.work_part.to_nx.Points.CreatePoint(NXOpen.Point3d(0.0, 0.0, 0.0))
		try:
			self.assertIsNotNone(UFManager.ask_point_data(point.Tag))
		finally:
			UFManager.delete_object(point.Tag)

	def test_create_line(self):
		line_tag = self.create_test_line()
		self.assertIsNotNone(line_tag)
		UFManager.delete_object(line_tag)

	def test_create_arc(self):
		arc_tag = self.create_test_arc()
		self.assertIsNotNone(arc_tag)
		UFManager.delete_object(arc_tag)

	def test_ask_part_units(self):
		self.assertIsNotNone(UFManager.ask_part_units(self.work_part.tag))

	def test_ask_work_coordinate_system(self):
		self.assertIsNotNone(UFManager.ask_work_coordinate_system())

	def test_set_work_coordinate_system(self):
		wcs_tag = UFManager.ask_work_coordinate_system()
		UFManager.set_work_coordinate_system(wcs_tag)
		self.assertEqual(UFManager.ask_work_coordinate_system(), wcs_tag)

	def test_ask_matrix_of_object(self):
		wcs_tag = UFManager.ask_work_coordinate_system()
		self.assertIsNotNone(UFManager.ask_matrix_of_object(wcs_tag))

	def test_open_listing_window(self):
		UFManager.open_listing_window()
		try:
			self.assertTrue(UFManager.is_listing_window_open())
		finally:
			UFManager.close_listing_window()

	def test_write_listing_window(self):
		UFManager.open_listing_window()
		try:
			UFManager.write_listing_window("UFManager integration test")
		finally:
			UFManager.close_listing_window()

	def test_close_listing_window(self):
		UFManager.open_listing_window()
		UFManager.close_listing_window()
		self.assertFalse(UFManager.is_listing_window_open())

	def test_is_listing_window_open(self):
		UFManager.open_listing_window()
		try:
			self.assertTrue(UFManager.is_listing_window_open())
		finally:
			UFManager.close_listing_window()

	def test_ask_display_color(self):
		result = UFManager.ask_display_color(1, NXOpen.UF.UFConstants.UF_DISP_rgb_model)
		self.assertIsNotNone(result)

	def test_set_display_color(self):
		color_model = NXOpen.UF.UFConstants.UF_DISP_rgb_model
		color_name, color_values = UFManager.ask_display_color(1, color_model)
		UFManager.set_display_color(1, color_model, color_name, color_values)

	def test_ask_work_view(self):
		self.assertIsNotNone(UFManager.ask_work_view())

	def test_fit_view(self):
		UFManager.fit_view(UFManager.ask_work_view(), 0.8)


if __name__ == "__main__":
	unittest.main()
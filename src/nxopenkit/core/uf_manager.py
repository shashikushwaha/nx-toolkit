from __future__ import annotations
import NXOpen

from nxopenkit.core.session import Session
# from enum import IntEnum
from typing import Tuple

# class UFObjectType(IntEnum):
# 	POINT = NXOpen.UF.UFConstants.UF_point_type
# 	LINE = NXOpen.UF.UFConstants.UF_line_type
# 	CIRCLE = NXOpen.UF.UFConstants.UF_circle_type
# 	CONIC = NXOpen.UF.UFConstants.UF_conic_type
# 	SPLINE = NXOpen.UF.UFConstants.UF_spline_type
# 	COORDINATE_SYSTEM = NXOpen.UF.UFConstants.UF_coordinate_system_type
# 	SOLID = NXOpen.UF.UFConstants.UF_solid_type
# 	FACE = NXOpen.UF.UFConstants.UF_face_type
# 	EDGE = NXOpen.UF.UFConstants.UF_edge_type
# 	DATUM_AXIS = NXOpen.UF.UFConstants.UF_datum_axis_type
# 	DATUM_PLANE = NXOpen.UF.UFConstants.UF_datum_plane_type
	# FEATURE = NXOpen.UF.UFConstants.UF_feature_type

# 	@classmethod
# 	def _missing_(cls, value: object) -> Optional["UFObjectType"]:
# 		if not isinstance(value, int):
# 			return None

# 		member = int.__new__(cls, value)
# 		member._name_ = "UF_TYPE_{}".format(value)
# 		member._value_ = value
# 		return member


class UFManager:
	"""Convenience wrappers for commonly used NX 2007 UF methods."""

	@staticmethod
	def ask_object_name(object_tag):
		return Session.uf_session().Obj.AskName(object_tag)

	@staticmethod
	def set_object_name(object_tag, name):
		return Session.uf_session().Obj.SetName(object_tag, name)

	@staticmethod
	def ask_object_type_and_subtype(object_tag) -> Tuple[int, int]:
		return Session.uf_session().Obj.AskTypeAndSubtype(object_tag)

	@staticmethod
	def ask_object_status(object_tag):
		return Session.uf_session().Obj.AskStatus(object_tag)

	@staticmethod
	def set_object_blank_status(object_tag, blank_status):
		return Session.uf_session().Obj.SetBlankStatus(object_tag, blank_status)

	@staticmethod
	def delete_object(object_id):
		return Session.uf_session().Obj.DeleteObject(object_id)

	@staticmethod
	def ask_body_type(body_tag):
		return Session.uf_session().Modeling.AskBodyType(body_tag)

	@staticmethod
	def ask_body_faces(body_tag):
		return Session.uf_session().Modeling.AskBodyFaces(body_tag)

	@staticmethod
	def ask_body_edges(body):
		return Session.uf_session().Modeling.AskBodyEdges(body)

	@staticmethod
	def ask_face_edges(face_tag):
		return Session.uf_session().Modeling.AskFaceEdges(face_tag)

	@staticmethod
	def ask_edge_vertices(edge_tag):
		return Session.uf_session().Modeling.AskEdgeVerts(edge_tag)

	@staticmethod
	def ask_edge_faces(edge):
		return Session.uf_session().Modeling.AskEdgeFaces(edge)
        

	@staticmethod
	def ask_face_data(face_tag):
		return Session.uf_session().Modeling.AskFaceData(face_tag)

	@staticmethod
	def ask_face_body(face):
		return Session.uf_session().Modeling.AskFaceBody(face)

	@staticmethod
	def ask_edge_type(edge_id):
		return Session.uf_session().Modeling.AskEdgeType(edge_id)

	@staticmethod
	def ask_face_type(face):
		return Session.uf_session().Modeling.AskFaceType(face)

	@staticmethod
	def ask_point_containment(point, body_tag):
		return Session.uf_session().Modeling.AskPointContainment(point, body_tag)

	@staticmethod
	def ask_minimum_distance(object1, object2, guess1_given, guess1, guess2_given, guess2):
		return Session.uf_session().Modeling.AskMinimumDist(
			object1, object2, guess1_given, guess1, guess2_given, guess2
		)

	@staticmethod
	def ask_bounding_box(object_tag):
		return Session.uf_session().ModlGeneral.AskBoundingBox(object_tag)

	@staticmethod
	def ask_aligned_bounding_box(object_arg, csys_tag, expand):
		return Session.uf_session().ModlGeneral.AskBoundingBoxAligned(object_arg, csys_tag, expand)

	@staticmethod
	def ask_exact_bounding_box(object_arg, csys_tag):
		return Session.uf_session().ModlGeneral.AskBoundingBoxExact(object_arg, csys_tag)

	@staticmethod
	def ask_curve_closed(curve_tag):
		return Session.uf_session().ModlGeneral.AskCurveClosed(curve_tag)

	@staticmethod
	def ask_curve_properties(curve_id, parameter):
		return Session.uf_session().ModlGeneral.AskCurveProps(curve_id, parameter)

	@staticmethod
	def ask_line_data(curve_tag):
		return Session.uf_session().Curve.AskLineData(curve_tag)

	@staticmethod
	def ask_arc_data(curve_tag):
		return Session.uf_session().Curve.AskArcData(curve_tag)

	@staticmethod
	def ask_point_data(point_tag):
		return Session.uf_session().Curve.AskPointData(point_tag)

	@staticmethod
	def create_line(line_coords : NXOpen.UF.Curve.Line):
		return Session.uf_session().Curve.CreateLine(line_coords)

	@staticmethod
	def create_arc(arc_coords: NXOpen.UF.Curve.Arc):
		return Session.uf_session().Curve.CreateArc(arc_coords)

	@staticmethod
	def ask_part_units(part_tag):
		return Session.uf_session().Part.AskUnits(part_tag)

	@staticmethod
	def ask_work_coordinate_system():
		return Session.uf_session().Csys.AskWcs()

	@staticmethod
	def set_work_coordinate_system(csys_tag):
		return Session.uf_session().Csys.SetWcs(csys_tag)

	@staticmethod
	def ask_matrix_of_object(object_id):
		return Session.uf_session().Csys.AskMatrixOfObject(object_id)

	@staticmethod
	def open_listing_window():
		return Session.uf_session().Ui.OpenListingWindow()

	@staticmethod
	def write_listing_window(text):
		return Session.uf_session().Ui.WriteListingWindow(text)

	@staticmethod
	def close_listing_window():
		return Session.uf_session().Ui.CloseListingWindow()

	@staticmethod
	def is_listing_window_open():
		return Session.uf_session().Ui.IsListingWindowOpen()

	@staticmethod
	def ask_display_color(color_number, color_model):
		return Session.uf_session().Disp.AskColor(color_number, color_model)

	@staticmethod
	def set_display_color(color_number, color_model, color_name, color_values):
		return Session.uf_session().Disp.SetColor(color_number, color_model, color_name, color_values)

	@staticmethod
	def ask_work_view():
		return Session.uf_session().View.AskWorkView()

	@staticmethod
	def fit_view(view_tag, fraction):
		return Session.uf_session().View.FitView(view_tag, fraction)





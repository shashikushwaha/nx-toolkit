import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxopenkit import Part
# from nxopenkit.core import part

class TestPart(unittest.TestCase): 

    def open_test_part(self, fixture_name):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases', fixture_name))
        self.part1 = Part.open_part(self.filePath)

    def tearDown(self):
        Part.close_all()

    def test_get_bodies(self):
        self.open_test_part('body.prt')
        allBodies = Part.bodies()
        print(allBodies[0])
        self.assertEqual(len(allBodies), 3)

    def test_get_faces(self):
        self.open_test_part('face.prt')
        allfaces = Part.faces()
        self.assertEqual(len(allfaces), 6)
    
    def test_get_edges(self):
        self.open_test_part('face.prt')
        allfaces = Part.edges()
        self.assertEqual(len(allfaces), 24)

    def test_get_displayable_objects(self):
        self.open_test_part('face.prt')
        all_displayables = Part.displayable_objects()
        self.assertEqual(len(all_displayables), 40)
        self.assertTrue(all(obj.nx_object is not None for obj in all_displayables))
    
    def test_get_part(self):
        self.open_test_part('part.prt')
        nxPart = self.part1.nx_object
        self.assertIsNotNone(nxPart)       

    def test_get_body_name(self):
        self.open_test_part('named-object.prt')
        body = Part.bodies("BODY_01")
        self.assertIsNotNone(body)   
        self.assertIsNotNone(body[0].nx_object)
    
    def test_failed_get_body_name(self):
        self.open_test_part('named-object.prt')
        with self.assertRaises(ValueError) as context:            
            body = Part.bodies("BODY_011")            
        self.assertEqual(str(context.exception), "BODY_011 not found.")  

    def test_get_points(self):
        self.open_test_part('points.prt')
        all_points = Part.points()
        self.assertEqual(len(all_points), 6)

    def test_get_point_name(self):
        self.open_test_part('points.prt')
        point = Part.points("POINT_04")
        self.assertIsNotNone(point)
        self.assertIsNotNone(point[0].nx_object)

    def test_get_curve(self):
        self.open_test_part('part.prt')
        all_curves = Part.curves()
        self.assertEqual(len(all_curves), 4)

    def test_get_curve_name(self):
        self.open_test_part('part.prt')
        curve = Part.curves("CURVE_01")
        self.assertIsNotNone(curve)
        self.assertIsNotNone(curve[0].nx_object)

    def test_get_datum_plane(self):
        self.open_test_part('part.prt')
        datum_plane = Part.datum_planes()
        self.assertEqual(len(datum_plane), 19)
        self.assertIsNotNone(datum_plane[0].nx_object)

    def test_get_csys(self):
        self.open_test_part('part.prt')
        datum_csys = Part.datum_csys()
        self.assertEqual(len(datum_csys), 6)
        self.assertIsNotNone(datum_csys[0].nx_object)

    def test_get_csys_by_name(self):
        self.open_test_part('part.prt')
        datum_csys = Part.datum_csys("CSYS_01")
        self.assertIsNotNone(datum_csys)
        self.assertIsNotNone(datum_csys[0].nx_object)

    def test_get_datum_axis(self):
        self.open_test_part('part.prt')
        datum_axis = Part.datum_axes()
        self.assertEqual(len(datum_axis), 18)

    def test_datum_plane_name(self):
        self.open_test_part('part.prt')
        datum_plane = Part.datum_planes("DATUM_02")
        self.assertIsNotNone(datum_plane)
        self.assertIsNotNone(datum_plane[0].nx_object)

    def test_datum_axis_name(self):
        self.open_test_part('part.prt')
        datum_axis = Part.datum_axes("AXIS_01")
        self.assertIsNotNone(datum_axis)
        self.assertIsNotNone(datum_axis[0].nx_object)

    def test_failed_get_datum_plane_name(self):
        self.open_test_part('part.prt')
        with self.assertRaises(ValueError) as context:            
            datum_plane = Part.datum_planes("DATUM_PLANE_011")            
        self.assertEqual(str(context.exception), "DATUM_PLANE_011 not found.")

    def test_failed_get_datum_axis_name(self):
        self.open_test_part('part.prt')
        with self.assertRaises(ValueError) as context:            
            datum_axis = Part.datum_axes("DATUM_AXIS_011")            
        self.assertEqual(str(context.exception), "DATUM_AXIS_011 not found.")

    def test_failed_get_curve_name(self):
        self.open_test_part('part.prt')
        with self.assertRaises(ValueError) as context:            
            curve = Part.curves("CURVE_011")            
        self.assertEqual(str(context.exception), "CURVE_011 not found.")

    def test_failed_get_point_name(self):
        self.open_test_part('points.prt')
        with self.assertRaises(ValueError) as context:            
            point = Part.points("POINT_011")            
        self.assertEqual(str(context.exception), "POINT_011 not found.")

    def test_failed_get_edge_name(self):
        self.open_test_part('face.prt')
        with self.assertRaises(ValueError) as context:            
            edge = Part.edges("EDGE_011")            
        self.assertEqual(str(context.exception), "EDGE_011 not found.")

    def test_failed_get_face_name(self):
        self.open_test_part('face.prt')
        with self.assertRaises(ValueError) as context:            
            face = Part.faces("FACE_011")            
        self.assertEqual(str(context.exception), "FACE_011 not found.") 

    def test_failed_get_body_name(self):
        self.open_test_part('named-object.prt')
        with self.assertRaises(ValueError) as context:            
            body = Part.bodies("BODY_011")            
        self.assertEqual(str(context.exception), "BODY_011 not found.")

    def test_failed_get_displayable_object_name(self):
        self.open_test_part('part.prt')
        with self.assertRaises(ValueError) as context:            
            displayable = Part.displayable_objects("DISPLAYABLE_011")            
        self.assertEqual(str(context.exception), "DISPLAYABLE_011 not found.")

    def test_get_displayable_object_name(self):
        self.open_test_part('face.prt')
        displayable = Part.displayable_objects("FACE_01")
        self.assertIsNotNone(displayable[0])
        self.assertIsNotNone(displayable[0].nx_object)

    def test_get_displayable_object_name_body(self):
        self.open_test_part('named-object.prt')
        displayable = Part.displayable_objects("BODY_01")
        self.assertIsNotNone(displayable[0])
        self.assertIsNotNone(displayable[0].nx_object)

    def test_get_displayable_object_name_point(self):
        self.open_test_part('points.prt')
        displayable = Part.displayable_objects("POINT_01")
        self.assertIsNotNone(displayable[0])
        self.assertIsNotNone(displayable[0].nx_object)

    def test_get_feature(self):
        self.open_test_part('part.prt')
        all_features = Part.features()
        self.assertEqual(len(all_features), 17)

    def test_get_feature_name(self):
        self.open_test_part('part.prt')
        feature = Part.features("CUBE")
        self.assertIsNotNone(feature[0])
        self.assertIsNotNone(feature[0].nx_object)


if __name__ == '__main__':
    unittest.main()        
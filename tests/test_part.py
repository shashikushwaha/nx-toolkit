import unittest
import os
import sys



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from build.lib.nxkit.core.body import Body
from nxkit import Part
# from nxkit.core import part

class TestPart(unittest.TestCase): 

    def open_test_part(self, fixture_name):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases', fixture_name))
        self.part1 = Part.open_part(self.filePath)

    def tearDown(self):
        Part.close_all()

    def test_get_bodies(self):
        self.open_test_part('body.prt')
        allBodies = Part.get_bodies()
        print(allBodies[0])
        self.assertEqual(len(allBodies), 3)

    def test_get_faces(self):
        self.open_test_part('face.prt')
        allfaces = Part.get_faces()
        self.assertEqual(len(allfaces), 6)
    
    def test_get_edges(self):
        self.open_test_part('face.prt')
        allfaces = Part.edges()
        self.assertEqual(len(allfaces), 24)

    def test_get_displayable_objects(self):
        self.open_test_part('face.prt')
        all_displayables = Part.get_displayable_objects()
        self.assertGreater(len(all_displayables), 0)
        self.assertTrue(all(obj.nx_object is not None for obj in all_displayables))
    
    def test_get_part(self):
        self.open_test_part('part.prt')
        nxPart = self.part1.nx_object
        self.assertIsNotNone(nxPart)       

    def test_get_body_name(self):
        self.open_test_part('named-object.prt')
        body = Part.get_body("BODY_01")
        self.assertIsNotNone(body)   
        self.assertIsNotNone(body.nx_object)
    
    def test_failed_get_body_name(self):
        self.open_test_part('named-object.prt')
        with self.assertRaises(ValueError) as context:            
            body = Part.get_body("BODY_011")            
        self.assertEqual(str(context.exception), "BODY_011 not found.")  

    def test_get_points(self):
        self.open_test_part('points.prt')
        all_points = Part.points()
        self.assertEqual(len(all_points), 4)
        self.assertTrue(all(point.nx_object is not None for point in all_points))

    def test_get_point_name(self):
        self.open_test_part('points.prt')
        point = Part.get_point("POINT_01")
        self.assertIsNotNone(point)
        self.assertIsNotNone(point.nx_object)

if __name__ == '__main__':
    unittest.main()        
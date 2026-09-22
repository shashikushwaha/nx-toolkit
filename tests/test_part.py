import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxtoolkit import Part

class TestPart(unittest.TestCase): 

    def setUp(self):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases', 'part.prt'))
        self.part1 = Part.OpenPart(self.filePath)

    def tearDown(self):
        Part.CloseAll()

    def test_get_bodies(self):
        allBodies = Part.GetBodies()
        print(allBodies[0])
        self.assertEqual( len(allBodies),1)

    def test_get_faces(self):
        allfaces = Part.GetFaces()
        self.assertEqual( len(allfaces),6)
    
    def test_get_edges(self):
        allfaces = Part.GetEdges()
        self.assertEqual( len(allfaces), 24)
    
    def test_get_part(self):
        nxPart = self.part1.nx_object
        self.assertIsNotNone(nxPart)       

if __name__ == '__main__':
    unittest.main()        
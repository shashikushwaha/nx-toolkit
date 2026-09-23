import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxkit import Part

class TestNamedObject(unittest.TestCase):

    def setUp(self):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases', 'named-object.prt'))
        self.part1 = Part.open_part(self.filePath)

    def tearDown(self):
        Part.close_all()

    def test_nammed_object(self):
        nxPart = self.part1.nx_object
        self.assertIsNotNone(nxPart)   
    
    def test_tagged_object(self):
        nxPart = self.part1.nx_object
        self.assertIsNotNone(nxPart)   

    def test_nx_object(self):
        self.assertIsNotNone(self.part1.nx_object)

    def test_tag(self):
        nxPart = self.part1.tag 
        self.assertIsNotNone(nxPart)     

    def test_name(self):
        all_bodies = Part.get_bodies(); 
        name = all_bodies[0].Name
        self.assertEqual(name, "BODY_01")  
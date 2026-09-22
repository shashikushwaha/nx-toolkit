import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxtoolkit import Body, Part

class TestBody(unittest.TestCase):
    def setUp(self):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases',  'body.prt'))
        self.part1 = Part.OpenPart(self.filePath)

    def tearDown(self):
        Part.CloseAll()
        
    def test_get_body_name(self):
        body = Body.BodyByName("BODY_01")
        self.assertIsNotNone(body)   
        self.assertIsNotNone(body.nx_object)

    def test_failed_get_body_name(self):
        with self.assertRaises(ValueError) as context:            
            body = Body.BodyByName("BODY_011")
            
        self.assertEqual(str(context.exception), "BODY_011 not found.")   
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxkit import Body, Part

class TestBody(unittest.TestCase):
    def setUp(self):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases',  'body.prt'))
        self.part1 = Part.open_part(self.filePath)

    def tearDown(self):
        Part.close_all()
        
   
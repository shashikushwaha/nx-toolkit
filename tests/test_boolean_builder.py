import unittest
import os
import sys
import NXOpen
import NXOpen.Features
import NXOpen.Features

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxopenkit import Body, Part, BooleanBuilder



class TestBooleanBuilder(unittest.TestCase):

    def setUp(self):
            self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases',  'body.prt'))
            self.part1 = Part.open_part(self.filePath)

    def tearDown(self):
        Part.close_all()

    def open_test_part(self, fixture_name):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases', fixture_name))
        self.part1 = Part.open_part(self.filePath)

    def test_boolean(self):
         self.open_test_part('boolean.prt')
         target_body = Part.bodies("Body_01")
         tool_bodies = Part.bodies()
         if target_body in tool_bodies:
            tool_bodies = tool_bodies.remove(target_body)
         boolBuilder = BooleanBuilder(target_body, tool_bodies, NXOpen.Features.Feature.BooleanType.Unite)
         boolBuilder.commit_feature()
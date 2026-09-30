import unittest
import os
import sys
import NXOpen
import NXOpen.Features
import NXOpen.Features

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxopenkit import Part, BooleanBuilder

class TestBooleanBuilder(unittest.TestCase):
    
    def open_test_part(self, fixture_name="body.prt"):
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases', fixture_name))
        self.part1 = Part.open_part(self.filePath)

    def tearDown(self):
        Part.close_all()

    def make_builder(self):
         self.open_test_part('body.prt')
         target_body = Part.bodies("BODY_01")
         tool_bodies = Part.bodies()
         if target_body[0] in tool_bodies:
            tool_bodies.remove(target_body[0])
         return BooleanBuilder(target_body[0], tool_bodies, NXOpen.Features.Feature.BooleanType.Unite)

    def test_rejects_empty_tool_bodies(self):
        with self.assertRaisesRegex(ValueError, "At least one tool body"):
            BooleanBuilder(None, [])

    def test_reject_empty_boolean_type(self):
        with self.assertRaisesRegex(ValueError, "boolean_type cannot be None"):
            BooleanBuilder(None, [object()], boolean_type=None)

    def test_settings_rejects_invalid_tolerance(self):
        builder = self.make_builder()

        for tolerance in (0, -0.1, float("nan"), float("inf"), -float("inf")):
            with self.subTest(tolerance= tolerance):
                with self.assertRaisesRegex(ValueError, "tolerance must be a finite positive number"):
                    builder.settings(tolerance=tolerance)

    def test_settings_without_tolerance(self):
        builder = self.make_builder()
        result = builder.settings(
            tolerance=None,
            keep_target=False, 
            keep_tool=True, 
            convert_to_sew=True)
        self.assertIs(result, builder)

    def test_boolean_unite_and_commit_feature(self):
        builder = self.make_builder()
        result = builder.settings(
            tolerance=0.0001,
            keep_target=True,
            keep_tool=False
        )
        self.assertIs(result, builder)
        feature = builder.commit_feature()
        self.assertIsNotNone(feature)

    def test_boolean_unite_and_commit(self):
        builder = self.make_builder()
        result = builder.settings(
            tolerance=0.0001,
            keep_target=True,
            keep_tool=False
        )
        self.assertIs(result, builder)
        feature = builder.commit()
        self.assertIsNotNone(feature)
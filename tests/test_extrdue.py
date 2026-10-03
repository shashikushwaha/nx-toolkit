import os
import sys
import unittest

import NXOpen

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxopenkit import ExtrudeBuilder, Part, Vector3d


class TestExtrudeBuilder(unittest.TestCase):
    def open_test_part(self, fixture_name="body.prt"):
        self.file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "test-cases", fixture_name)
        )
        self.part = Part.open_part(self.file_path)

    def tearDown(self):
        Part.close_all()

    def make_builder(self, distance=10.0):
        self.open_test_part()
        edges = Part.faces("FACE_016")[0].get_edges()
        return ExtrudeBuilder(edges, "0", 10, direction=Vector3d(0, 0, 1))

    def test_rejects_empty_profile_curves(self):
        with self.assertRaisesRegex(ValueError, "At least one profile curve"):
            ExtrudeBuilder([], 10.0)


    def test_rejects_invalid_direction(self):
        for direction in (
            Vector3d(0.0, 0.0, 0.0),
            Vector3d(float("nan"), 0.0, 1.0),
        ):
            with self.subTest(direction=direction):
                with self.assertRaises(ValueError):
                    ExtrudeBuilder([object()], 1.0, 10, direction)


    def test_settings_update_distance_and_return_builder(self):
        builder = self.make_builder()
        result = builder.settings(NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet, tolerance=0.0001)
        self.assertIs(result, builder)
        self.assertEqual(builder.nx_builder.FeatureOptions.BodyType , NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Sheet)
        feature = builder.commit_feature()
        self.assertIsNotNone(feature)
        
    def test_extrude_and_commit_feature(self):
        builder = self.make_builder()
        feature = builder.commit_feature()
        filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-cases','temp','test.prt'))
        Part.save_as(filePath)
        self.assertIsNotNone(feature)

    def test_extrude_and_commit(self):
        builder = self.make_builder()
        committed_objects = builder.commit()
        self.assertTrue(committed_objects)


if __name__ == "__main__":
    unittest.main()
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
try:
    import NXOpen  # noqa: F401
except Exception as exc:  # pragma: no cover
    pytest.skip(f"NXOpen unavailable or incompatible in this environment: {exc}", allow_module_level=True)
from nxopenkit.core.part import Part


@pytest.fixture
def named_part():
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "test-cases", "named-object.prt")
    )
    part = Part.open_part(file_path)
    try:
        yield part
    finally:
        Part.close_all()


class TestNamedObject:
    def test_named_object(self, named_part):
        assert named_part.to_nx is not None

    def test_tagged_object(self, named_part):
        assert named_part.to_nx is not None

    def test_nx_object(self, named_part):
        assert named_part.to_nx is not None

    def test_tag(self, named_part):
        assert named_part.tag is not None

    def test_name(self, named_part):
        all_bodies = Part.get_bodies()
        name = all_bodies[0].name
        assert name == "BODY_01"
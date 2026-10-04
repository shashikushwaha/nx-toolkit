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
def body_part():
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "test-cases", "body.prt")
    )
    part = Part.open_part(file_path)
    try:
        yield part
    finally:
        Part.close_all()


class TestBody:
    def test_body_part_loads(self, body_part):
        assert body_part is not None

   
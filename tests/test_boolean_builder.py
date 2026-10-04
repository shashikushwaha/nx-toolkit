import os
import sys

import pytest

try:
    import NXOpen
    import NXOpen.Features
except Exception as exc:  # pragma: no cover
    pytest.skip(f"NXOpen unavailable or incompatible in this environment: {exc}", allow_module_level=True)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from nxopenkit.core.part import  Part
from nxopenkit.modeling.boolean_builder import BooleanBuilder


@pytest.fixture
def builder_factory():
    def _make_builder(boolean_type=NXOpen.Features.Feature.BooleanType.Unite):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "test-cases", "body.prt")
        )
        Part.open_part(file_path)
        target_body = Part.get_bodies("BODY_01")
        tool_bodies = Part.get_bodies()
        if target_body[0] in tool_bodies:
            tool_bodies.remove(target_body[0])
        return BooleanBuilder(target_body[0], tool_bodies, boolean_type)

    yield _make_builder
    Part.close_all()


class TestBooleanBuilder:
    def test_rejects_empty_tool_bodies(self):
        with pytest.raises(ValueError, match="At least one tool body"):
            BooleanBuilder(None, [])

    def test_reject_empty_boolean_type(self):
        with pytest.raises(ValueError, match="boolean_type cannot be None"):
            BooleanBuilder(None, [object()], boolean_type=None)

    def test_settings_rejects_invalid_tolerance(self, builder_factory):
        builder = builder_factory()

        for tolerance in (0, -0.1, float("nan"), float("inf"), -float("inf")):
            with pytest.raises(ValueError, match="tolerance must be a finite positive number"):
                builder.settings(tolerance=tolerance)

    def test_settings_without_tolerance(self, builder_factory):
        builder = builder_factory()
        result = builder.settings(
            tolerance=None,
            keep_target=False,
            keep_tool=True,
            convert_to_sew=True,
        )
        assert result is builder

    def test_boolean_unite_and_commit_feature(self, builder_factory):
        builder = builder_factory()
        result = builder.settings(
            tolerance=0.0001,
            keep_target=True,
            keep_tool=False,
        )
        assert result is builder
        feature = builder.commit_feature()
        assert feature is not None

    def test_boolean_unite_and_commit(self, builder_factory):
        builder = builder_factory()
        result = builder.settings(
            tolerance=0.0001,
            keep_target=True,
            keep_tool=False,
        )
        assert result is builder
        feature = builder.commit()
        assert feature is not None

    def test_boolean_intersect_and_commit_feature(self, builder_factory):
        builder = builder_factory(boolean_type=NXOpen.Features.Feature.BooleanType.Intersect)
        assert builder.nx_builder.Operation == NXOpen.Features.Feature.BooleanType.Intersect
        feature = builder.commit_feature()
        assert feature is not None

    def test_boolean_subtract_and_commit_feature(self, builder_factory):
        builder = builder_factory(boolean_type=NXOpen.Features.Feature.BooleanType.Subtract)
        assert builder.nx_builder.Operation == NXOpen.Features.Feature.BooleanType.Subtract
        feature = builder.commit_feature()
        assert feature is not None


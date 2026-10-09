from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING

import NXOpen
import NXOpen.Features
# import NXOpen.GeometricUtilities

from .feature_builder import FeatureBuilder
from nxopenkit.core.part import Part
from nxopenkit.core.body import Body
from .decorators import builder_operation
logger = logging.getLogger(__name__)
# if TYPE_CHECKING:
#     from nxopenkit.core.body import Body


# KeepRemoveOption = (
#     NXOpen.GeometricUtilities.BooleanRegionSelect.KeepRemoveOption
# )


class BooleanBuilder(FeatureBuilder):
    def __init__(
        self,
        target_body: Body,
        tool_bodies: Sequence[Body],
        boolean_type: NXOpen.Features.Feature.BooleanType = NXOpen.Features.Feature.BooleanType.Unite
    ):
        if not tool_bodies:
            raise ValueError("At least one tool body is required.")
        if boolean_type is None:
            raise ValueError("boolean_type cannot be None.")

        super().__init__()

        self.target_body = target_body
        self.tool_bodies = list(tool_bodies)
        self.boolean_type = boolean_type

        work_part = Part.work_part().to_nx
        target_nx = target_body.to_nx
        tool_nx_bodies = [body.to_nx for body in self.tool_bodies]
        self._set_undo_mark()
        try:
            self._booleanBld = work_part.Features.CreateBooleanBuilderUsingCollector( NXOpen.Features.BooleanFeature.Null)
            
            self.feature_builder = self._booleanBld
            self.builder = self._booleanBld
            self._booleanBld.Tolerance = self.distance_tolerance
            self._booleanBld.Operation = boolean_type
            self._booleanBld.Targets.Add(target_nx)
            self._booleanBld.BooleanRegionSelect.AssignTargets([target_nx])
            collector = work_part.ScCollectors.CreateCollector()
            body_rule = work_part.ScRuleFactory.CreateRuleBodyDumb(
                tool_nx_bodies, True
            )
            collector.ReplaceRules([body_rule], False)
            self._booleanBld.ToolBodyCollector = collector
        except Exception:
            logger.exception("Failed creating BooleanBuilder")
            if self._extrudeBld is not None:
                self._destroy()
            raise

    @property
    def nx_builder(self) -> NXOpen.Features.BooleanBuilder:
        return self._booleanBld
    
    # @builder_operation
    # def region(
    #     self,
    #     keep_remove_target: KeepRemoveOption = KeepRemoveOption.Keep,
    #     keep_remove_tool: KeepRemoveOption = KeepRemoveOption.Keep,
    # ) -> BooleanBuilder:
    #     region_select = self.booleanBuilder1.BooleanRegionSelect
    #     region_select.KeepRemoveTargetMethod = keep_remove_target
    #     region_select.KeepRemoveToolMethod = keep_remove_tool
    #     return 
    
    @builder_operation
    def settings(
        self,
        tolerance: float | None = None,
        keep_target: bool = False,
        keep_tool: bool = False,
        convert_to_sew: bool = False,
    ) -> BooleanBuilder:                
        self._validate_tolerance(tolerance)
        self._booleanBld.Tolerance = self.distance_tolerance
        self._booleanBld.CopyTargets = keep_target
        self._booleanBld.CopyTools = keep_tool
        self._booleanBld.ConvertToSew = convert_to_sew
        return self
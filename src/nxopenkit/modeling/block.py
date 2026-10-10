from __future__ import annotations

from collections.abc import Sequence

import logging
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities

from nxopenkit.core.datum_axis import DatumAxis
from nxopenkit.core.body import Body
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.part import Part
from nxopenkit.core.direction import Direction
from nxopenkit.core.point import Point
from nxopenkit.maths.vector3d import Vector3d
from .decorators import builder_operation

from .feature_builder import FeatureBuilder
logger = logging.getLogger(__name__)

class Block(FeatureBuilder):

    def __init__(
        self,
        type : NXOpen.Features.BlockFeatureBuilder.Types,
        origin_point : Point,
        second_point : Point = None,
        xc_length: int | float | str = 100,
        yc_length: int | float | str = 100,
        zc_length: int | float | str = 100,
    ):
        
        self.type = type
        self.origin_point = origin_point.to_nx
        self.xc_length = str(xc_length)
        self.yc_length = str(yc_length)
        self.zc_length = str(zc_length)
        super().__init__()        

        work_part = Part.work_part().to_nx
        self._set_undo_mark()
        try:
            self._blockBld = work_part.Features.CreateBlockFeatureBuilder(NXOpen.Features.Feature.Null)           

            self.feature_builder = self._blockBld
            self.builder = self._blockBld
            self._blockBld.OriginPoint = self.origin_point
            if(self.type == NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths):

                self._blockBld.SetOriginAndLengths(self.origin_point.Coordinates, self.xc_length, self.yc_length, self.zc_length)

        except Exception:
            self._destroy()
            raise

    @property
    def nx_builder(self) -> NXOpen.Features.BlockFeatureBuilder:
        return self._blockBld


    @builder_operation
    def boolean(
        self,
        boolean_option:
        NXOpen.GeometricUtilities.BooleanOperation.BooleanType,
        boolean_target_body: Sequence[Body],
    ) -> Block:
        if (boolean_option != NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create and not boolean_target_body):
            raise ValueError("Target bodies are required for Unite, Subtract, and Intersect operations.")

        self._blockBld.BooleanOperation.Type = boolean_option
        self._blockBld.BooleanOperation.SetTargetBodies([body.to_nx for body in boolean_target_body])

        return self

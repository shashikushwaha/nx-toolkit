from __future__ import annotations
from collections.abc import Sequence

import logging
import NXOpen as nx
import NXOpen.Features
import NXOpen.GeometricUtilities

from nxopenkit.core.converters import to_nx_axis
from nxopenkit.core.validators import validate_positive_double
from nxopenkit.core.datum_axis import DatumAxis
from nxopenkit.core.body import Body
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.part import Part
from nxopenkit.core.direction import Direction
from nxopenkit.core.point import Point
from nxopenkit.core.types import Double, VectorLike
from nxopenkit.maths.vector3d import Vector3d
from ..core.decorators import builder_operation

from .feature_builder import FeatureBuilder
logger = logging.getLogger(__name__)

class Cylinder(FeatureBuilder):

    def __init__(
        self,
        type: nx.Features.CylinderBuilder.Types,
        height: Double,
        origin_point: Point | None = None,
        vector: VectorLike | None = None,
        diameter: Double = 25,
        arc: ICurve | None = None,
    ):
        if height is None:
            raise ValueError(f"height is required for type {type}")
        
        if type == nx.Features.CylinderBuilder.Types.AxisDiameterAndHeight:

            if origin_point is None:
                raise ValueError(f"origin_point is required for type {type}")

            if vector is None:
                raise ValueError(f"vector is required for type {type}")
            
            if diameter is None:
                raise ValueError(f"diameter is required for type {type}")
            
        if type == NXOpen.Features.CylinderBuilder.Types.ArcAndHeight:
            if arc is None:
                raise ValueError(f"arc is required for type {type}")
            
        if origin_point is not None:
            self.origin_point = origin_point.to_nx

        self.type = type
        self.axis = to_nx_axis(vector,is_mandatory=False)
        self.diameter = str(validate_positive_double(diameter,"diameter"))       
        self.height = str(validate_positive_double(height,"height",))

        super().__init__()     

        work_part = Part.work_part().to_nx
        self._set_undo_mark()
        try:
            self._cylinderBld = work_part.Features.CreateCylinderBuilder(nx.Features.Feature.Null)           

            self.feature_builder = self._cylinderBld
            self.builder = self._cylinderBld
            self._cylinderBld.Origin = self.origin_point
            self._cylinderBld.Type = self.type
            if(self.type == nx.Features.CylinderBuilder.Types.ArcAndHeight):
                self._cylinderBld.Arc.SetValue(self.origin_point.Coordinates, self.xc_length, self.yc_length, self.zc_height_length)

            elif(self.type == nx.Features.CylinderBuilder.Types.AxisDiameterAndHeight):
                self._cylinderBld.Height = self.height
                self._cylinderBld.Diameter = self.diameter
                self._cylinderBld.Axis = self.axis
                self._cylinderBld.Axis.Point = self.origin_point
            
        except Exception:
            self._destroy()
            raise

    @property
    def nx_builder(self) -> NXOpen.Features.BlockFeatureBuilder:
        return self._cylinderBld


    @builder_operation
    def boolean(
        self,
        boolean_option: NXOpen.Features.Feature.BooleanType,
        boolean_target_body: Body,
    ) -> Cylinder:
        if (boolean_option != NXOpen.Features.Feature.BooleanType.Create and not boolean_target_body):
            raise ValueError("Target bodies are required for Unite, Subtract, and Intersect operations.")

        self._cylinderBld.SetBooleanOperationAndTarget(boolean_option, boolean_target_body.to_nx )
        return self

    @builder_operation
    def settings(self, associate_origin : bool = True) -> Cylinder :        
            self._cylinderBld.ParentAssociativity = associate_origin
            return self
        

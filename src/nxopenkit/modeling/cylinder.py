from __future__ import annotations
import logging
from typing import Sequence
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities

from nxopenkit.core.converters import to_nx_axis
from nxopenkit.core.validators import validate_positive_double
from nxopenkit.core.body import Body
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.part import Part
from nxopenkit.core.point import Point
from nxopenkit.core.types import BooleanType, CylinderType, Double, VectorLike
from nxopenkit.core.decorators import builder_operation
from nxopenkit.core.enum_utils import get_enum_name

from .feature_builder import FeatureBuilder
logger = logging.getLogger(__name__)

class Cylinder(FeatureBuilder):

    def __init__(
        self,
        cly_type: CylinderType,
        height: Double,
        origin_point: Point | None = None,
        vector: VectorLike | None = None,
        diameter: Double = 25,
        arc: ICurve | None = None,
    ):

        type_name = get_enum_name(CylinderType,cly_type)
        if height is None:
            raise ValueError(f"height is required for type {type_name}")
        
        if cly_type == CylinderType.AxisDiameterAndHeight:

            if origin_point is None:
                raise ValueError(f"origin_point is required for type {type_name}")

            if vector is None:
                raise ValueError(f"vector is required for type {type_name}")
            
            if diameter is None:
                raise ValueError(f"diameter is required for type {type_name}")
            
        elif cly_type == CylinderType.ArcAndHeight:
            if arc is None:
                raise ValueError(f"arc is required for type {type_name}")
            
        if origin_point is not None:
            self.origin_point = origin_point.to_nx

        self.type = cly_type
        self.axis = to_nx_axis(vector,is_mandatory=False)
        self.diameter = str(validate_positive_double(diameter,"diameter"))       
        self.height = str(validate_positive_double(height,"height",))
        

        super().__init__()     

        work_part = Part.work_part().to_nx
        self._set_undo_mark()
        try:
            self._cylinderBld = work_part.Features.CreateCylinderBuilder(NXOpen.Features.Feature.Null)           

            self.feature_builder = self._cylinderBld
            self.builder = self._cylinderBld            
            self._cylinderBld.Type = self.type
            self._cylinderBld.Height.SetFormula(self.height)
            if(self.type == CylinderType.ArcAndHeight):
                self.arc = arc.to_nx
                self._cylinderBld.Arc.Value = self.arc

            elif(self.type == CylinderType.AxisDiameterAndHeight):
                self._cylinderBld.Origin = self.origin_point.Coordinates
                self._cylinderBld.Diameter.SetFormula(self.diameter)
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
        boolean_option: BooleanType,
        boolean_target_body: Sequence[Body],
    ) -> Cylinder:
        if (boolean_option != BooleanType.Create and not boolean_target_body):
            raise ValueError("Target bodies are required for Unite, Subtract, and Intersect operations.")
        self._cylinderBld.BooleanOption.Type = boolean_option
        self._cylinderBld.BooleanOption.SetTargetBodies([body.to_nx  for body in boolean_target_body] )
        return self

    @builder_operation
    def settings(self, associate_origin : bool = True) -> Cylinder :        
            self._cylinderBld.ParentAssociativity = associate_origin
            return self
        

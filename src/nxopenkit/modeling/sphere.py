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
from nxopenkit.core.types import BooleanType, Double, SphereType, VectorLike
from nxopenkit.core.decorators import builder_operation
from nxopenkit.core.enum_utils import get_enum_name

from .feature_builder import FeatureBuilder
logger = logging.getLogger(__name__)

class Sphere(FeatureBuilder):

    def __init__(
        self,
        spr_type: SphereType,
        center_point: Point | None = None,
        diameter: Double = 25,
        arc: ICurve | None = None,
    ):

        type_name = get_enum_name(SphereType,spr_type)
        if spr_type == SphereType.Arc:

            if arc is None:
                raise ValueError(f"arc is required for type {type_name}")
            self.arc = arc.to_nx

        elif spr_type == SphereType.CenterPointAndDiameter:
             if center_point is None:
                raise ValueError(f"center point is required for type {type_name}")
             
             self.center_point = center_point.to_nx

            

        self.type = spr_type
        self.diameter = str(diameter)
        super().__init__()     

        work_part = Part.work_part().to_nx
        self._set_undo_mark()
        try:
            self._sphereBld = work_part.Features.CreateSphereBuilder(NXOpen.Features.Sphere.Null)           

            self.feature_builder = self._sphereBld
            self.builder = self._sphereBld            
            self._sphereBld.Type = self.type
            if(self.type == SphereType.Arc):                
                self._sphereBld.Arc.Value = self.arc
            elif(self.type == SphereType.CenterPointAndDiameter):
                self._sphereBld.CenterPoint = self.center_point
                self._sphereBld.Diameter.SetFormula(self.diameter)
            
        except Exception:
            self._destroy()
            raise

    @property
    def nx_builder(self) -> NXOpen.Features.SphereBuilder:
        return self._sphereBld


    @builder_operation
    def boolean(
        self,
        boolean_option: BooleanType,
        boolean_target_body: Sequence[Body],
    ) -> Sphere:
        if (boolean_option != BooleanType.Create and not boolean_target_body):
            raise ValueError("Target bodies are required for Unite, Subtract, and Intersect operations.")
        self._sphereBld.BooleanOption.Type = boolean_option
        self._sphereBld.BooleanOption.SetTargetBodies([body.to_nx  for body in boolean_target_body] )
        return self

    @builder_operation
    def settings(self, associate_origin : bool = True) -> Sphere :        
            self._sphereBld.ParentAssociativity = associate_origin
            return self
        

from __future__ import annotations

import math
from collections.abc import Sequence
from turtle import distance
from turtle import distance
from typing import TYPE_CHECKING
from unittest import case

import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from nxopenkit.core.body import Body
from nxopenkit.core.icurve import ICurve
from nxopenkit.maths.vector3d import Vector3d
from .feature_builder import FeatureBuilder
from nxopenkit.core.part import Part

# if TYPE_CHECKING:
#     from nxopenkit.core.curve import Curve


class ExtrudeBuilder(FeatureBuilder):
    def __init__(
        self,
        curves: Sequence[ICurve],
        start_distance: str | float,
        end_distance: str | float | None = None,
        direction: Vector3d = Vector3d(0.0, 0.0, 1.0),
    ):
        if not curves:
            raise ValueError("At least one profile curve is required.")
                
        if not math.isfinite(float(start_distance)):
            raise ValueError("distance must be a finite positive number.")        

        if not math.isfinite(float(end_distance)):
                raise ValueError("end_distance must be a finite positive number.")
    
        self.curves = list(curves)
        self.start_distance = start_distance
        self.end_distance = end_distance
        self.direction = direction
        direction = direction.normalize()
        nx_curves = [curve.to_nx for curve in self.curves]
        super().__init__()
        work_part = Part.work_part().to_nx
        self._extrudeBld = work_part.Features.CreateExtrudeBuilder(NXOpen.Features.Feature.Null)
        self.feature_builder = self._extrudeBld
        self.builder = self._extrudeBld
        self._extrudeBld.Limits.EndExtend.SetValue(str(end_distance))
        self._extrudeBld.Limits.StartExtend.SetValue(str(start_distance))        
        section = work_part.Sections.CreateSection(
            self.chaining_tolerance,
            self.distance_tolerance,
            self.angle_tolerance,
        )
        section.SetAllowedEntityTypes(NXOpen.Section.AllowTypes.OnlyCurves)
        curve_rule = work_part.ScRuleFactory.CreateRuleBaseCurveDumb(nx_curves)
        section.AddToSection(
            [curve_rule],
            nx_curves[0],
            None,
            None,
            NXOpen.Point3d(0.0, 0.0, 0.0),
            NXOpen.Section.Mode.Create,
            False,
        )       

        self._extrudeBld.Section = section
        self._extrudeBld.Direction = work_part.Directions.CreateDirection(
            NXOpen.Point3d(0.0, 0.0, 0.0),
            direction.to_nx,
            NXOpen.SmartObject.UpdateOption.WithinModeling
        )

    @property
    def nx_builder(self) -> NXOpen.Features.ExtrudeBuilder:
        return self._extrudeBld
    
    def settings(
        self,
        body_type: NXOpen.GeometricUtilities.FeatureOptions.BodyStyle = NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Solid,
        tolerance: float | None = None        
    ) -> ExtrudeBuilder:
        
        if tolerance is not None:
            if not math.isfinite(tolerance) or tolerance <= 0:
                raise ValueError("tolerance must be a finite positive number.")
        if tolerance is None:
            self.distance_tolerance = self.distance_tolerance
        
        self._extrudeBld.DistanceTolerance = self.distance_tolerance 
        self._extrudeBld.ChainingTolerance = 0.95*self.distance_tolerance 
        self._extrudeBld.AngularTolerance = self.angle_tolerance
        self._extrudeBld.FeatureOptions.BodyType = body_type
        return self

    def offset(
            self, offset_option: NXOpen.GeometricUtilities.Type,
            end_offset: float | str,
            start_offset: float | str | None = None) -> ExtrudeBuilder:
        if offset_option is NXOpen.GeometricUtilities.Type.NonsymmetricOffset and (start_offset is None or end_offset is None):
            raise ValueError("Both start_offset and end_offset must be provided for nonsymmetric offset.")
        if (offset_option is NXOpen.GeometricUtilities.Type.SingleOffset or offset_option is NXOpen.GeometricUtilities.Type.SymmetricOffset) and start_offset is None:
                raise ValueError("Only end_offset must be provided for symmetric offset.")
        self._extrudeBld.Offset.Type = offset_option
        self._extrudeBld.Offset.EndOffset = end_offset
        self._extrudeBld.Offset.StartOffset = start_offset
        return self

    def boolean(
              self,
              boolean_option: NXOpen.GeometricUtilities.BooleanOperation.BooleanType,
              boolean_target_body: Sequence[Body]) -> ExtrudeBuilder:
        if boolean_option is not NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create and len(boolean_target_body)  == 0:
            raise ValueError("boolean_target_body should be empty when boolean_option is Create.")

        self._extrudeBld.BooleanOperation.Type = boolean_option
        self._extrudeBld.BooleanOperation.SetTargetBodies([body.to_nx for body in boolean_target_body])
        return self

    def draft(
        self,
        draft_type: NXOpen.GeometricUtilities.SimpleDraft.SimpleDraftType,
        draft_angle: float | str,        
        draft_vector: Vector3d | None = None
    ) -> ExtrudeBuilder:
        self._extrudeBld.Draft.DraftOption = draft_type
        self._extrudeBld.Draft.DraftAngle.Value = draft_angle
        if draft_vector is not None:
            self._extrudeBld.Draft.Vector = draft_vector.to_nx
        return self
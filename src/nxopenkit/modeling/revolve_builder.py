from __future__ import annotations

from collections.abc import Sequence

import logging
import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities

from nxopenkit.core.datum_axis import DatumAxis
from nxopenkit.core.body import Body
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.part import Part
from nxopenkit.core.direction import Direction
from nxopenkit.maths.vector3d import Vector3d
from .decorators import builder_operation

from .feature_builder import FeatureBuilder
logger = logging.getLogger(__name__)

class RevolveBuilder(FeatureBuilder):

    def __init__(
        self,
        curves: Sequence[ICurve],
        direction: DatumAxis | Direction | Vector3d,
        start_angle: float | str = 0,
        end_angle: float | str = 360,
    ):

        if not curves:
            raise ValueError("At least one profile curve is required.")
        

        self.curves = list(curves)
        self.axis = self._to_datum_axis(direction)
        self.start_angle = start_angle
        self.end_angle = end_angle
        super().__init__()        

        work_part = Part.work_part().to_nx
        self._set_undo_mark()
        try:
            self._revolveBld = work_part.Features.CreateRevolveBuilder(NXOpen.Features.Feature.Null)           

            self.feature_builder = self._revolveBld
            self.builder = self._revolveBld

            section = work_part.Sections.CreateSection(
                self.chaining_tolerance,
                self.distance_tolerance,
                self.angle_tolerance,
            )
            section.SetAllowedEntityTypes( NXOpen.Section.AllowTypes.OnlyCurves)

            nx_curves = [ curve.to_nx for curve in self.curves]

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

            self._revolveBld.Section = section           
            self._revolveBld.Limits.StartExtend.Value.SetFormula(str(start_angle))           
            self._revolveBld.Limits.EndExtend.Value.SetFormula(str(end_angle))

        except Exception:
            self._destroy()
            raise

    @builder_operation
    def settings(
        self,
        body_type: NXOpen.GeometricUtilities.FeatureOptions.BodyStyle = NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Solid,
        tolerance: float | None = None,
    ) -> RevolveBuilder:
        self._validate_tolerance(tolerance)
        self._revolveBld.DistanceTolerance = self.distance_tolerance
        self._revolveBld.ChainingTolerance = self.chaining_tolerance
        self._revolveBld.AngularTolerance = self.angle_tolerance
        self._revolveBld.FeatureOptions.BodyType = body_type
        return self

    @builder_operation
    def boolean(
        self,
        boolean_option:
        NXOpen.GeometricUtilities.BooleanOperation.BooleanType,
        boolean_target_body: Sequence[Body],
    ) -> RevolveBuilder:
        if (boolean_option != NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create and not boolean_target_body):
            raise ValueError("Target bodies are required for Unite, Subtract, and Intersect operations.")

        self._revolveBld.BooleanOperation.Type = boolean_option
        self._revolveBld.BooleanOperation.SetTargetBodies([body.to_nx for body in boolean_target_body])

        return self
    
    @builder_operation
    def angles(
        self,
        start_angle: float | str,
        end_angle: float | str,
    ) -> RevolveBuilder:
        self._revolveBld.Limits.StartExtend.SetValue(str(start_angle))
        self._revolveBld.Limits.EndExtend.SetValue(str(end_angle))
        return self
    
    @builder_operation
    def offset(
        self,
        offset_option: NXOpen.GeometricUtilities.Type,
        end_offset: float | str,
        start_offset: float | str | None = None,
    ) -> RevolveBuilder:

        if (offset_option == NXOpen.GeometricUtilities.Type.NonsymmetricOffset and start_offset is None):
            raise ValueError("start_offset is required for NonsymmetricOffset.")

        self._revolveBld.Offset.Option = offset_option
        self._revolveBld.Offset.SetEndOffset(str(end_offset))
        if start_offset is not None:
            self._revolveBld.Offset.SetStartOffset(str(start_offset))
            
        return self

    def _to_datum_axis(
    self,
    axis: DatumAxis | Direction | Vector3d,
    ) -> DatumAxis:

        if isinstance(axis, DatumAxis):
            return axis
        work_part = Part.work_part().to_nx
        if isinstance(axis, Vector3d):
            nx_direction = (
                    work_part.Directions.CreateDirection(
                    NXOpen.Point3d(0.0, 0.0, 0.0),
                    axis.to_nx,
                    NXOpen.SmartObject.UpdateOption.WithinModeling,
                )
            )

            nx_axis = (
                    work_part.Axes.CreateAxis(
                    NXOpen.Point.Null,
                    nx_direction,
                    NXOpen.SmartObject.UpdateOption.WithinModeling,
                )
            )

            return DatumAxis(nx_axis)

        if isinstance(axis, Direction):

            nx_axis = (
                    work_part.Axes.CreateAxis(
                    NXOpen.Point.Null,
                    axis.to_nx,
                    NXOpen.SmartObject.UpdateOption.WithinModeling,
                )
            )

            return DatumAxis(nx_axis)

        raise TypeError("direction must be DatumAxis, Direction, or Vector3d.")
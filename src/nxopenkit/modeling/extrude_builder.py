from __future__ import annotations

import logging
import math
from collections.abc import Sequence

import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities

from nxopenkit.core.body import Body
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.part import Part
from nxopenkit.maths.vector3d import Vector3d

from .feature_builder import FeatureBuilder
from .decorators import builder_operation


logger = logging.getLogger(__name__)


class ExtrudeBuilder(FeatureBuilder):
    def __init__(
        self,
        curves: Sequence[ICurve],
        start_distance: str | float,
        end_distance: str | float | None = None,
        direction: Vector3d = Vector3d(0.0, 0.0, 1.0),
    ):
        if not curves:
            raise ValueError(
                "At least one profile curve is required."
            )

        self.curves = list(curves)
        self.start_distance = start_distance
        self.end_distance = end_distance
        self.direction = direction.normalize()

        self._extrudeBld: NXOpen.Features.ExtrudeBuilder | None = None

        nx_curves = [curve.to_nx for curve in self.curves]

        super().__init__()

        work_part = Part.work_part().to_nx
        self._set_undo_mark()
        try:
            self._extrudeBld = work_part.Features.CreateExtrudeBuilder(NXOpen.Features.Feature.Null)
            self.feature_builder = self._extrudeBld
            self.builder = self._extrudeBld

            self._extrudeBld.Limits.StartExtend.SetValue(str(start_distance))

            if end_distance is not None:
                self._extrudeBld.Limits.EndExtend.SetValue(str(end_distance))

            section = work_part.Sections.CreateSection(
                self.chaining_tolerance,
                self.distance_tolerance,
                self.angle_tolerance,
            )

            section.SetAllowedEntityTypes(NXOpen.Section.AllowTypes.OnlyCurves)
            curve_rule = (work_part.ScRuleFactory.CreateRuleBaseCurveDumb(nx_curves))
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
                    self.direction.to_nx,
                    NXOpen.SmartObject.UpdateOption.WithinModeling,
                )            

        except Exception:
            logger.exception("Failed creating ExtrudeBuilder")
            if self._extrudeBld is not None:
                self._destroy()
            raise

    @property
    def nx_builder(self) -> NXOpen.Features.ExtrudeBuilder:
        if self._extrudeBld is None:
            raise RuntimeError("ExtrudeBuilder has not been initialized.")
        return self._extrudeBld

    @builder_operation
    def settings(
        self,
        body_type: NXOpen.GeometricUtilities.FeatureOptions.BodyStyle = NXOpen.GeometricUtilities.FeatureOptions.BodyStyle.Solid,
        tolerance: float | None = None,
    ) -> ExtrudeBuilder:

        self._validate_tolerance(tolerance)
        self._extrudeBld.DistanceTolerance = self.distance_tolerance
        self._extrudeBld.ChainingTolerance = self.chaining_tolerance
        self._extrudeBld.AngularTolerance = self.angle_tolerance
        self._extrudeBld.FeatureOptions.BodyType = body_type 
        return self

    @builder_operation
    def offset(
        self,
        offset_option: NXOpen.GeometricUtilities.Type,
        end_offset: float | str,
        start_offset: float | str | None = None,
    ) -> ExtrudeBuilder:
        if (offset_option == NXOpen.GeometricUtilities.Type.NonsymmetricOffset and start_offset is None):
            raise ValueError("start_offset is required for NonsymmetricOffset.")

        self._extrudeBld.Offset.Option = offset_option
        self._extrudeBld.Offset.SetEndOffset(str(end_offset))
        if start_offset is not None:
            self._extrudeBld.Offset.SetStartOffset(str(start_offset))

        return self

    @builder_operation
    def boolean(
        self,
        boolean_option: NXOpen.GeometricUtilities.BooleanOperation.BooleanType,
        boolean_target_body: Sequence[Body],
    ) -> ExtrudeBuilder:

        if (boolean_option != NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create
            and not boolean_target_body):
            raise ValueError("Target bodies are required for Unite, Subtract, and Intersect operations.")

        self._extrudeBld.BooleanOperation.Type = boolean_option
        self._extrudeBld.BooleanOperation.SetTargetBodies([body.to_nx for body in boolean_target_body])

        return self
    
    @builder_operation
    def draft(
        self,
        draft_type: NXOpen.GeometricUtilities.SimpleDraft.SimpleDraftType,
        draft_angle: float | str,
        draft_option: NXOpen.GeometricUtilities.MultiDraft.AngleOption | None = None,
    ) -> ExtrudeBuilder:
        self._extrudeBld.Draft.DraftOption = draft_type
        self._extrudeBld.Draft.DraftAngle.SetFormula(str(draft_angle))
        if draft_option is not None:
            self._extrudeBld.Draft.SetAngleOption(draft_option)

        return self
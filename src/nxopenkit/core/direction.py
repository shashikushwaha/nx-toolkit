from __future__ import annotations

from typing import cast

import NXOpen
from nxopenkit.maths.point3d import Point3d
from nxopenkit.maths.vector3d import Vector3d
# from nxopenkit.core import direction
from .part import Part
from .displayable_object import DisplayableObject

class Direction(DisplayableObject):

    def __init__(self, direction : NXOpen.Direction):
        self._direction = direction
        super().__init__(direction)

    @property
    def to_nx(self) -> NXOpen.Direction:
        return cast(NXOpen.Direction, super().to_nx)

    @staticmethod
    def create_direction_from_vector(
        origin: Point3d,
        vector: Vector3d,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

       direction = Part.work_part().to_nx.Directions.CreateDirection(
                   origin.to_nx,
                   vector.to_nx,
                   update_option
        )
       return Direction(direction)

    @staticmethod
    def create_direction_from_line(
        line: NXOpen.Line,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            line,
            sense,
            update_option
        )
        return Direction(direction)
    
    @staticmethod
    def create_direction_from_edge(
        edge: NXOpen.IBaseCurve,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            edge,
            sense,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_conic(
        conic: NXOpen.Conic,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            conic,
            sense,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_axis(
        axis: NXOpen.DatumAxis,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            axis,
            sense,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_face_normal(
        face: NXOpen.IParameterizedSurface,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":
        direction = Part.work_part().to_nx.Directions.CreateDirection(
            face,
            sense,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_plane_normal(
        plane: NXOpen.IBasePlane,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            plane,
            sense,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_sketch_normal(
        sketch: NXOpen.Sketch,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            sketch,
            sense,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_points(
        start_point: NXOpen.Point,
        end_point: NXOpen.Point,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            start_point,
            end_point,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_control_points(
        start_point: NXOpen.Routing.ControlPoint,
        end_point: NXOpen.Routing.ControlPoint,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":

        direction = Part.work_part().to_nx.Directions.CreateDirection(
            start_point,
            end_point,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_curve_parameter(
        curve: NXOpen.IBaseCurve,
        parameter: NXOpen.Scalar,
        option: NXOpen.Direction.OnCurveOption,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":
        direction = Part.work_part().to_nx.Directions.CreateDirection(
            curve,
            parameter,
            option,
            sense,
            update_option
        )
        return Direction(direction)
        
    @staticmethod
    def create_direction_from_curve_point(
        curve: NXOpen.IBaseCurve,
        point: NXOpen.Point,
        option: NXOpen.Direction.OnCurveOption,
        sense=NXOpen.Sense.Forward,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":
        direction = Part.work_part().to_nx.Directions.CreateDirection(
            curve,
            point,
            option,
            sense,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_transform(
        direction: NXOpen.Direction,
        xform: NXOpen.Xform,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":
        direction = Part.work_part().to_nx.Directions.CreateDirection(
            direction,
            xform,
            update_option
        )
        return Direction(direction)

    @staticmethod
    def create_direction_from_combine(
        direction1: NXOpen.Direction,
        direction2: NXOpen.Direction,
        update_option: NXOpen.SmartObject.UpdateOption = NXOpen.SmartObject.UpdateOption.WithinModeling
    ) -> "Direction":
        direction = Part.work_part().to_nx.Directions.CreateDirection(
            direction1,
            direction2,
            update_option
        )
        return Direction(direction)
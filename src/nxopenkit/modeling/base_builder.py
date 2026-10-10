import math
from typing import Union
import NXOpen
from nxopenkit.core.datum_axis import DatumAxis
from nxopenkit.core.direction import Direction
from nxopenkit.core.part import Part
from nxopenkit.maths.vector3d import Vector3d



class BaseBuilder():
    def __init__(self):
        self.session : NXOpen.Session = Part.session()
        self.work_part: Part = Part.work_part()
        self.builder : NXOpen.Builder = None
        self.undo_mark_id : int = None
        self.undo_mark_name : str = ""
        self.distance_tolerance : float = self.work_part.to_nx.Preferences.Modeling.DistanceToleranceData
        self.chaining_tolerance : float = 0.95*self.distance_tolerance
        self.angle_tolerance : float = self.work_part.to_nx.Preferences.Modeling.AngleToleranceData

    def _destroy(self):
        if(self.builder is not None):
            self.builder.Destroy()
            self.builder = None

    def _set_undo_mark(self):
        self.undo_mark_id = self.session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, self.undo_mark_name)


    def _undo_mark(self):
        self.session.UndoToMark(self.undo_mark_id, self.undo_mark_name)
        self.session.DeleteUndoMark(self.undo_mark_id, self.undo_mark_name)

    def _validate_tolerance(self, tolerance: float) -> None:
        if tolerance is None:
            return
        
        if(tolerance is not None):
            if (not math.isfinite(tolerance) or tolerance <= 0 ):
                raise ValueError("tolerance must be a finite positive number.")
        self.distance_tolerance = tolerance
        self.chaining_tolerance = 0.95*tolerance

    def _to_datum_axis(self, axis: Union[DatumAxis, Direction, Vector3d]):
        work_part = Part.work_part().to_nx
        if isinstance(axis, DatumAxis):
            direction1 = work_part.Directions.CreateDirection(axis.to_nx, NXOpen.Sense.Forward, NXOpen.SmartObject.UpdateOption.WithinModeling)    
            axis1 = work_part.Axes.CreateAxis(NXOpen.Point.Null, direction1, NXOpen.SmartObject.UpdateOption.WithinModeling)
            return axis1
        
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

            return nx_axis

        if isinstance(axis, Direction):

            nx_axis = (
                    work_part.Axes.CreateAxis(
                    NXOpen.Point.Null,
                    axis.to_nx,
                    NXOpen.SmartObject.UpdateOption.WithinModeling,
                )
            )

            return nx_axis

        raise TypeError("direction must be DatumAxis, Direction, or Vector3d.")
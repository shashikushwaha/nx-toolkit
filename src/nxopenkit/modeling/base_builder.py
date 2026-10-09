import math
import sys
import NXOpen
import os
from nxopenkit.core.part import Part



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
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

    def destroy(self):
        if(self.builder is not None):
            self.builder.Destroy()
            self.builder = None

    def undo_mark(self):
        self.session.UndoToMark(self.undo_mark_id, self.undo_mark_name)
        self.session.DeleteUndoMark(self.undo_mark_id, self.undo_mark_name)
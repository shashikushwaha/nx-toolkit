from __future__ import annotations
from typing import Sequence, cast
import NXOpen
from nxopenkit.core.session import Session
from nxopenkit.maths.point3d import Point3d
from .displayable_object import DisplayableObject
from .icurve import ICurve


class Curve(DisplayableObject, ICurve):
    def __init__(self, nxCurve):
        super().__init__(nxCurve)

    @property
    def to_nx(self) -> NXOpen.Curve:
        return cast(NXOpen.Curve, super().to_nx)

    @staticmethod
    def create_composite_curve(curves_edges :Sequence[ICurve], help_point : Point3d = Point3d(0,0,0)) -> Curve:
        if curves_edges is None:
            raise ValueError(f"curves_edges is required.")
        nx_icurve = [base.to_nx for base in curves_edges]
        work_part =  Session.work_part()
        selectionIntentRuleOptions1 = work_part.ScRuleFactory.CreateRuleOptions()    
        selectionIntentRuleOptions1.SetSelectedFromInactive(False)    
        icurve_rule = work_part.ScRuleFactory.CreateRuleBaseCurveDumb(nx_icurve, selectionIntentRuleOptions1)    
        selectionIntentRuleOptions1.Dispose()
        distance_tolerance : float = work_part.Preferences.Modeling.DistanceToleranceData
        chaining_tolerance : float = 0.95*distance_tolerance
        angle_tolerance : float = work_part.Preferences.Modeling.AngleToleranceData
        section1 = work_part.Sections.CreateSection(chaining_tolerance, distance_tolerance, angle_tolerance)
        section1.AllowSelfIntersection(True)
        rules1 = [None] * 1 
        rules1[0] = icurve_rule
        section1.AddToSection(rules1, nx_icurve[0], nx_icurve[0], NXOpen.NXObject.Null, help_point.to_nx, NXOpen.Section.Mode.Create, False)
        comp_curve = Session.work_part().Curves.CreateSmartCompositeCurve(section1, NXOpen.SmartObject.UpdateOption.WithinModeling, distance_tolerance)
        return Curve(comp_curve)





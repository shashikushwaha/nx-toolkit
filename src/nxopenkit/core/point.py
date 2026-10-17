from __future__ import annotations
from typing import Sequence, cast
import NXOpen
import NXOpen.Features
# import NXOpen.GeometricUtilities

from nxopenkit.core.face import Face
from nxopenkit.core.icurve import ICurve
from nxopenkit.core.curve import Curve
from nxopenkit.core.session import Session
from nxopenkit.core.types import Double, PointOnCurveLocationOption
from nxopenkit.maths.point3d import Point3d
from .displayable_object import DisplayableObject

class Point(DisplayableObject):
    def __init__(self, nxPoint ):
        super().__init__(nxPoint)

    @property
    def to_nx(self) -> NXOpen.Point:
        return cast(NXOpen.Point, super().to_nx)

    @property
    def coordinates(self) -> Point3d :
         return Point3d.from_nx(self.to_nx.Coordinates)

    @staticmethod
    def create_point(coordinate : Point3d) -> Point:
        return Point(NXOpen.Session.GetSession().Parts.Work.Points.CreatePoint(coordinate.to_nx))
    
    @staticmethod
    def create_point_on_Edge_Curve(
        curves_edges :Sequence[ICurve],
        percentage : Double,
        location_option : PointOnCurveLocationOption = PointOnCurveLocationOption.PercentArcLength,
        help_point : Point3d = Point3d(0,0,0),
        ) -> Point:
    
        if curves_edges is None:
                raise ValueError(f"curves_edges is required.")
        # nx_icurve = [one_cr.to_nx for one_cr in curves_edges]
        
        comp_curve = Curve.create_composite_curve(curves_edges=curves_edges, help_point=help_point)
        sclr_expr = Session.work_part().Expressions.CreateSystemExpression(str(percentage))
        scalar = Session.work_part().Scalars.CreateScalarExpression(sclr_expr, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        nx_point = NXOpen.Session.GetSession().Parts.Work.Points.CreatePoint(
            comp_curve.to_nx,
            scalar,
            location_option,
            NXOpen.SmartObject.UpdateOption.WithinModeling,

        )
        return Point(nx_point)

    @staticmethod
    def create_point_on_face(face : Face, u_value : Double = 0.5, v_value : Double = 0.5):
        u_expr = Session.work_part().Expressions.CreateSystemExpression(str(u_value))
        u_scalar = Session.work_part().Scalars.CreateScalarExpression(u_expr, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        v_expr = Session.work_part().Expressions.CreateSystemExpression(str(v_value))
        v_scalar = Session.work_part().Scalars.CreateScalarExpression(v_expr, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        nx_point = NXOpen.Session.GetSession().Parts.Work.Points.CreatePoint(
            face.to_nx,
            u_scalar,
            v_scalar,
            NXOpen.SmartObject.UpdateOption.WithinModeling,    
            )
        return Point(nx_point)

    @staticmethod
    def create_point_between_points(point1 : Point, point2 : Point, percentage_location : Double = 50):
        loc_expr = Session.work_part().Expressions.CreateSystemExpression(str(percentage_location))
        loc_scalar = Session.work_part().Scalars.CreateScalarExpression(loc_expr, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        nx_point = NXOpen.Session.GetSession().Parts.Work.Points.CreatePoint(
            point1.to_nx,
            point2.to_nx,
            loc_scalar,
            NXOpen.SmartObject.UpdateOption.WithinModeling,    
            )
        return Point(nx_point)



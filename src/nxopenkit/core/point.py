from __future__ import annotations
from typing import cast, TYPE_CHECKING
import sys
import NXOpen as nx
from nxopenkit.maths.point3d import Point3d
from .displayable_object import DisplayableObject

class Point(DisplayableObject):
    def __init__(self, nxPoint ):
        super().__init__(nxPoint)

    @property
    def to_nx(self) -> nx.Point:
        return cast(nx.Point, super().to_nx)

    @staticmethod
    def create_point(coordinate : Point3d) -> Point:
        return Point(nx.Session.GetSession().Parts.Work.Points.CreatePoint(coordinate.to_nx))
    





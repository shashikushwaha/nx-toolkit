import sys
from typing import cast
import NXOpen
from .displayable_object import DisplayableObject
from .icurve import ICurve


class Edge(DisplayableObject, ICurve):
    def __init__(self, nxEdge ):
        super().__init__(nxEdge)

    @property
    def to_nx(self) -> NXOpen.Edge:
        return cast(NXOpen.Edge, super().to_nx)

    def get_body(self) -> "Body":
        from .body import Body
        return Body(self.to_nx.GetBody())
    





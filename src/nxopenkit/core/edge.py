from __future__ import annotations
from typing import cast, TYPE_CHECKING
import NXOpen
from .displayable_object import DisplayableObject
from .icurve import ICurve

if TYPE_CHECKING:
    from .body import Body


class Edge(DisplayableObject, ICurve):
    def __init__(self, nxEdge ):
        super().__init__(nxEdge)

    @property
    def to_nx(self) -> NXOpen.Edge:
        return cast(NXOpen.Edge, super().to_nx)

    def get_body(self) -> Body:
        from .body import Body
        return Body(self.to_nx.GetBody())
    





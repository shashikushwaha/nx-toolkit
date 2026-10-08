from __future__ import annotations
import NXOpen
from typing import List, cast, TYPE_CHECKING
from .displayable_object import DisplayableObject
from .isurface import ISurface
from .edge import Edge

if TYPE_CHECKING:
    from .body import Body

class Face(DisplayableObject, ISurface):
    def __init__(self, nxDisplayableObject):
        super().__init__(nxDisplayableObject)

    @property
    def to_nx(self) -> NXOpen.Face:
        return cast(NXOpen.Face, super().to_nx)

    def get_edges(self) -> List[Edge]:
        return [Edge(edge) for edge in self.to_nx.GetEdges()]

    def get_body(self) -> Body:
        from .body import Body
        return Body(self.to_nx.GetBody())

    



import sys
import NXOpen
from typing import List, cast

from .edge import Edge
from .face import Face
from .displayable_object import DisplayableObject


class Body(DisplayableObject):
    def __init__(self, nxBody : NXOpen.Body):
        super().__init__(nxBody)

    @property
    def to_nx(self) -> NXOpen.Body:
        return cast(NXOpen.Body, super().to_nx)

    def faces(self) -> List[Face] :
        return [Face(face) for face in self.to_nx.GetFaces()]

    def edges(self) -> List[Edge] :
        return [Edge(edge) for edge in self.to_nx.GetEdges()]

    # def __str__(self):
    #     return (f"{self.Name}, {self.Tag}")   
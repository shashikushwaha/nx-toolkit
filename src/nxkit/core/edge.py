import sys
from typing import cast
import NXOpen
from .displayable_object import DisplayableObject


class Edge(DisplayableObject):
    def __init__(self, nxEdge ):
        super().__init__(nxEdge)

    @property
    def nx_object(self) -> NXOpen.Edge:
        return cast(NXOpen.Edge, super().nx_object)
    





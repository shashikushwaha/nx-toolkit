from typing import cast
import sys
import NXOpen
from .displayable_object import DisplayableObject


class CoordinateSystem(DisplayableObject):
    def __init__(self, nxCsys ):
        super().__init__(nxCsys)

    @property
    def nx_object(self) -> NXOpen.CoordinateSystem:
        return cast(NXOpen.CoordinateSystem, super().nx_object)
    





from typing import cast
import sys
import NXOpen
from .displayable_object import DisplayableObject


class Point(DisplayableObject):
    def __init__(self, nxPoint ):
        super().__init__(nxPoint)

    @property
    def to_nx(self) -> NXOpen.Point:
        return cast(NXOpen.Point, super().to_nx)
    





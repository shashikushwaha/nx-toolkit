from typing import cast
import sys
import NXOpen
from .displayable_object import DisplayableObject


class DatumAxis(DisplayableObject):
    def __init__(self, nxDatumAxis ):
        super().__init__(nxDatumAxis)

    @property
    def nx_object(self) -> NXOpen.DatumAxis:
        return cast(NXOpen.DatumAxis, super().nx_object)
    





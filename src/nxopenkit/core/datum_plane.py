from typing import cast
import sys
import NXOpen
from .displayable_object import DisplayableObject
from .isurface import ISurface


class DatumPlane(DisplayableObject, ISurface):
    def __init__(self, nxDatumPlane ):
        super().__init__(nxDatumPlane)

    @property
    def nx_object(self) -> NXOpen.DatumPlane:
        return cast(NXOpen.DatumPlane, super().nx_object)
    





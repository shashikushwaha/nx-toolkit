from typing import cast
import sys
import NXOpen
from .displayable_object import DisplayableObject
from .isurface import ISurface


class DatumPlane(DisplayableObject, ISurface):
    def __init__(self, nxDatumPlane ):
        super().__init__(nxDatumPlane)

    @property
    def to_nx(self) -> NXOpen.DatumPlane:
        return cast(NXOpen.DatumPlane, super().to_nx)
    





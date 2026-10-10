from typing import cast
import NXOpen
from .displayable_object import DisplayableObject


class DatumAxis(DisplayableObject):
    def __init__(self, nxDatumAxis ):
        super().__init__(nxDatumAxis)

    @property
    def to_nx(self) -> NXOpen.DatumAxis:
        return cast(NXOpen.DatumAxis, super().to_nx)
    





from typing import cast
import sys
import NXOpen
from .displayable_object import DisplayableObject
from .icurve import ICurve


class Curve(DisplayableObject, ICurve):
    def __init__(self, nxCurve):
        super().__init__(nxCurve)

    @property
    def to_nx(self) -> NXOpen.Curve:
        return cast(NXOpen.Curve, super().to_nx)





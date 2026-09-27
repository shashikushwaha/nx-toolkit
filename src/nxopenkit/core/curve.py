from typing import cast
import sys
import NXOpen
from .displayable_object import DisplayableObject
from .icurve import ICurve


class Curve(DisplayableObject, ICurve):
    def __init__(self, nxCurve):
        super().__init__(nxCurve)

    @property
    def nx_object(self) -> NXOpen.Curve:
        return cast(NXOpen.Curve, super().nx_object)





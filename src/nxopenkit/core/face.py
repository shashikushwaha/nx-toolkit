import sys
import NXOpen
from typing import List, cast
from .displayable_object import DisplayableObject
from .isurface import ISurface

class Face(DisplayableObject, ISurface):
    def __init__(self, nxDisplayableObject):
        super().__init__(nxDisplayableObject)

    @property
    def nx_object(self) -> NXOpen.Face:
        return cast(NXOpen.Face, super().nx_object)
    



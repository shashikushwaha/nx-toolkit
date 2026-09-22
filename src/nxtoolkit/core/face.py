import sys
import NXOpen
from .displayable_object import DisplayableObject

class Face(DisplayableObject):
    def __init__(self, nxDisplayableObject):
        super().__init__(nxDisplayableObject)

    @property
    def nx_object(self) -> NXOpen.Face:
        return super().nx_object


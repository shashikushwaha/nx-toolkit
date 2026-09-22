import sys
import NXOpen
from .named_object import NamedObject

class DisplayableObject(NamedObject):

    def __init__(self, nxDisplayableObject : NXOpen.DisplayableObject):
        super().__init__(nxDisplayableObject)

    @property
    def nx_object(self) -> NXOpen.DisplayableObject:
        return super().nx_object
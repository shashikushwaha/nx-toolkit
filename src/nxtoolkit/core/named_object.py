import sys
import math
import NXOpen
from typing import List
from .tagged_object import TaggedObject


class NamedObject(TaggedObject):
    def __init__(self, nxobject: NXOpen.NXObject):
        super().__init__(nxobject)

    @property
    def nx_object(self) -> NXOpen.NXObject:
        return super().nx_object

    @property
    def Name(self) ->str :
        return self.nx_object.Name

import sys
import math
import NXOpen
from typing import List, cast
from .tagged_object import TaggedObject


class NamedObject(TaggedObject):
    def __init__(self, nxobject: NXOpen.NXObject):
        super().__init__(nxobject)

    @property
    def to_nx(self) -> NXOpen.NXObject:
        return cast(NXOpen.NXObject, self.tagged_object)

    @property
    def name(self) ->str :
        return self.to_nx.Name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self.to_nx.SetName(value)

    

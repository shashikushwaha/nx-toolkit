import sys
from .named_object import NamedObject
from .body import Body
from typing import List, cast
import NXOpen
import NXOpen_Features


class Feature(NamedObject):
    def __init__(self, nxFeature: NXOpen_Features.Feature):
        super().__init__(nxFeature)

    @property
    def to_nx(self) -> NXOpen_Features.Feature:
        return cast(NXOpen_Features.Feature, super().to_nx)

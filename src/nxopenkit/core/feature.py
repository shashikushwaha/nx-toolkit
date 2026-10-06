import sys
from .named_object import NamedObject
from .body import Body
from typing import List, cast
import NXOpen
import NXOpen.Features


class Feature(NamedObject):
    def __init__(self, nxFeature: NXOpen.Features.Feature):
        super().__init__(nxFeature)

    @property
    def to_nx(self) -> NXOpen.Features.Feature:
        return cast(NXOpen.Features.Feature, super().to_nx)

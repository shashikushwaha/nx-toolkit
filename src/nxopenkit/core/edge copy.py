import sys
from typing import cast
import NXOpen
from .displayable_object import DisplayableObject
from .named_object import NamedObject



class Feature(NamedObject):
    def __init__(self, nx_feature ):
        super().__init__(nx_feature)

    @property
    def nx_object(self) -> NXOpen.Features.Feature:
        return cast(NXOpen.Features.Feature, super().nx_object)
    





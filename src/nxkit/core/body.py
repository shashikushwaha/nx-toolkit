import sys
import NXOpen
from typing import List, cast
from .displayable_object import DisplayableObject


class Body(DisplayableObject):
    def __init__(self, nxBody : NXOpen.Body):
        super().__init__(nxBody)

    @property
    def nx_object(self) -> NXOpen.Body:
        return cast(NXOpen.Body, super().nx_object)



    # def __str__(self):
    #     return (f"{self.Name}, {self.Tag}")   
import sys
from typing import cast
import NXOpen
from .named_object import NamedObject

class DisplayableObject(NamedObject):

    def __init__(self, nxDisplayableObject : NXOpen.DisplayableObject):
        super().__init__(nxDisplayableObject)

    @property
    def nx_object(self) -> NXOpen.DisplayableObject:
        return cast(NXOpen.DisplayableObject, super().nx_object)

    @staticmethod
    def get_by_name(name: str) -> "DisplayableObject":
        
        all_displayable_objects : NXOpen.DisplayableObject = NXOpen.Session.GetSession().Parts.Work.AppearanceManager
        allObjects = [obj for obj in all_displayable_objects if(obj.Name == name)]
        if(len(allObjects) == 0):
            raise ValueError(f"{name} not found.") 
        return DisplayableObject(allObjects[0])
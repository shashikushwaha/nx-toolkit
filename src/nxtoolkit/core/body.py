import sys
import NXOpen
from .displayable_object import DisplayableObject


class Body(DisplayableObject):
    def __init__(self, nxBody : NXOpen.Body):
        super().__init__(nxBody)

    @property
    def nx_object(self) -> NXOpen.Body:
        return super().nx_object

    @staticmethod
    def BodyByName(name: str) -> "Body":
        bodiesCol : NXOpen.BodyCollection = NXOpen.Session.GetSession().Parts.Work.Bodies
        allBodies = [onebody for onebody in bodiesCol if(onebody.Name == name)]
        if(len(allBodies) == 0):
            raise ValueError(f"{name} not found.") 
        return Body(allBodies[0])

    # def __str__(self):
    #     return (f"{self.Name}, {self.Tag}")   
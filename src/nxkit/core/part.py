import sys
import math

from numpy import var
import NXOpen
from typing import List

from nxkit.core.point import Point
from .named_object import NamedObject
from .body import Body
from .displayable_object import DisplayableObject
from .edge import Edge
from .face import Face
from .point import Point
from typing import cast

class Part(NamedObject) :    
    def __init__(self, nxOpenPart : NXOpen.Part):      
        self.session = NXOpen.Session.GetSession()
        self.workPart = self.session.Parts.Work 
        super().__init__(nxOpenPart)    

    @property
    def nx_object(self) -> NXOpen.Part:
        return cast(NXOpen.Part, super().nx_object)

    @staticmethod
    def open_part(filePath)-> "Part":

        results = NXOpen.Session.GetSession().Parts.OpenActiveDisplay(filePath, NXOpen.DisplayPartOption.AllowAdditional)
        openPart = results[0]
        part1 = Part(openPart)   
        return part1    
    
    @staticmethod
    def close_all():
        theSession : NXOpen.Session = NXOpen.Session.GetSession()
        partCloseRes : NXOpen.PartCloseResponses = theSession.Parts.NewPartCloseResponses()
        theSession.Parts.CloseAll(NXOpen.BasePart.CloseModified.CloseModified, partCloseRes)
        partCloseRes.Dispose()    

    @staticmethod
    def get_bodies() -> List[Body]:
        bodiesCol = NXOpen.Session.GetSession().Parts.Work.Bodies
        all_bodies = []
        for one_body in bodiesCol:
            all_bodies.append(Body(one_body))       
        return all_bodies    

    @staticmethod
    def get_faces() -> List[Face]:
        allbodies = Part.get_bodies()
        # allFaces = [];
        allFaces = [Face(face) for body in allbodies for face in body.nx_object.GetFaces()]
        # for body in allbodies:
        #     for face in body.nx_object.GetFaces():
        #         allFaces.append(face)      

        return allFaces
    @staticmethod
    def edges() -> List[Edge]:
        allfaces : List[Face] = Part.get_faces() 
        allEdges = [Edge(edge) for face in allfaces for edge in face.nx_object.GetEdges()]
        return allEdges

    @staticmethod
    def points() -> List[Point]:
        workPart : NXOpen.Part = NXOpen.Session.GetSession().Parts.Work
        point_col = workPart.Points
        all_points = []
        for one_point in point_col:
            print(one_point.Name)
            all_points.append(one_point)
        return all_points


    @staticmethod
    def get_displayable_objects() -> List[DisplayableObject]:
        all_displayables: List[DisplayableObject] = []
        all_displayables.extend(Part.get_bodies())
        all_displayables.extend(Part.get_faces())
        all_displayables.extend(Part.edges())
        all_displayables.extend(Part.points())

        return all_displayables

    @staticmethod
    def get_body(name: str) -> Body:
        bodies_Col : List[Body] = Part.get_bodies()
        allBodies = [onebody for onebody in bodies_Col if(onebody.Name == name)]
        if(len(allBodies) == 0):
            raise ValueError(f"{name} not found.") 
        return allBodies[0]
            
    @staticmethod
    def get_face(name: str) -> Face:
        all_faces : List[Face] = Part.get_faces()
        allFaces = [oneface for oneface in all_faces if(oneface.Name == name)]
        if(len(allFaces) == 0):
            raise ValueError(f"{name} not found.") 
        return allFaces[0]

    @staticmethod
    def get_edge(name: str) -> Edge:
        all_edges : List[Edge] = Part.edges()
        allEdges = [one_edge for one_edge in all_edges if(one_edge.Name == name)]
        if(len(allEdges) == 0):
            raise ValueError(f"{name} not found.") 
        return Edge(allEdges[0])

    @staticmethod
    def get_point(name: str) -> Point:
        all_points = Part.points()
        allPoints = [one_point for one_point in all_points if(one_point.Name == name)]
        if(len(allPoints) == 0):
            raise ValueError(f"{name} not found.") 
        return allPoints[0]
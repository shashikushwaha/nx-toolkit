import sys
import math

# from numpy import var
import NXOpen
import NXOpen.UF

from typing import List, Optional
from .named_object import NamedObject
from .body import Body
from .displayable_object import DisplayableObject
from .edge import Edge
from .face import Face
from .point import Point
from .datum_plane import DatumPlane
from .datum_axis import DatumAxis
from .curve import Curve
from .coordinate_system import CoordinateSystem
from typing import cast
from .feature import Feature

class Part(NamedObject) :    
    def __init__(self, nxOpenPart : NXOpen.Part):      
        self.session = NXOpen.Session.GetSession()
        self.workPart = self.session.Parts.Work 
        super().__init__(nxOpenPart)    

    @property
    def nx_object(self) -> NXOpen.Part:
        return cast(NXOpen.Part, super().nx_object)

    @staticmethod
    def session() -> NXOpen.Session:
        return NXOpen.Session.GetSession()

    @staticmethod
    def uf_session() -> NXOpen.UF.UFSession:
        return NXOpen.UF.UFSession.GetUFSession()

    @staticmethod
    def work_part() -> NXOpen.Part:
        workPart : NXOpen.Part = Part.session().Parts.Work
        if(workPart is None):
            raise ValueError("No work part found. check NX License.")
        return workPart

    @staticmethod
    def open_part(filePath)-> "Part":
        results = Part.session().Parts.OpenActiveDisplay(filePath, NXOpen.DisplayPartOption.AllowAdditional)
        openPart = results[0]
        part1 = Part(openPart)   
        return part1    
    
    @staticmethod
    def close_all():
        theSession : NXOpen.Session = Part.session()
        partCloseRes : NXOpen.PartCloseResponses = theSession.Parts.NewPartCloseResponses()
        theSession.Parts.CloseAll(NXOpen.BasePart.CloseModified.CloseModified, partCloseRes)
        partCloseRes.Dispose() 


    @staticmethod
    def bodies(name: Optional[str] = None) -> List[Body]:
        bodiesCol = Part.work_part().Bodies
        all_bodies = []
        for one_body in bodiesCol:
            all_bodies.append(Body(one_body))
        if name is None:
            return all_bodies
        matching_bodies = [body for body in all_bodies if body.Name == name]
        if not matching_bodies:
            raise ValueError(f"{name} not found.")
        return matching_bodies

    @staticmethod
    def faces(name: Optional[str] = None) -> List[Face]:
        all_bodies = Part.bodies()
        all_faces = [Face(face) for body in all_bodies for face in body.nx_object.GetFaces()]
        if name is None:
            return all_faces
        matching_faces = [face for face in all_faces if face.Name == name]
        if not matching_faces:
            raise ValueError(f"{name} not found.")
        return matching_faces
    
    @staticmethod
    def edges(name: Optional[str] = None) -> List[Edge]:
        all_edges = [
            Edge(edge)
            for body in Part.work_part().Bodies
            for face in body.GetFaces()
            for edge in face.GetEdges()
        ]
        if name is None:
            return all_edges

        matching_edges = [edge for edge in all_edges if edge.Name == name]
        if not matching_edges:
            raise ValueError(f"{name} not found.") 
        return matching_edges
    
    @staticmethod
    def points(name: Optional[str] = None) -> List[Point]:
        work_part = Part.work_part()
        point_collection : NXOpen.PointCollection = work_part.Points
        all_points = []
        for one_point in point_collection:
            all_points.append(Point(one_point))
        if name is None:
            return all_points
        matching_points = [point for point in all_points if point.Name == name]
        if not matching_points:
            raise ValueError(f"{name} not found.")
        return matching_points


    @staticmethod
    def displayable_objects(name: Optional[str] = None) -> List[DisplayableObject]:
        all_displayables: List[DisplayableObject] = []
        all_displayables.extend(Part.bodies())
        all_displayables.extend(Part.faces())
        all_displayables.extend(Part.edges())
        all_displayables.extend(Part.points())
        all_displayables.extend(Part.curves())
        all_displayables.extend(Part.datum_planes())
        all_displayables.extend(Part.datum_csys())  
        all_displayables.extend(Part.datum_axes())
        if name is None:
            return all_displayables
        matching_displayables = [obj for obj in all_displayables if obj.Name == name]
        if not matching_displayables:
            raise ValueError(f"{name} not found.")
        return matching_displayables


    
    @staticmethod
    def features(name: Optional[str] = None) -> List[NXOpen.Features.Feature]:
        feature_collection : NXOpen.Features.FeatureCollection = Part.work_part().Features
        all_features = []
        for one_feature in feature_collection:
            all_features.append(Feature(one_feature))
        if name is None:
            return all_features
        matching_features = [feature for feature in all_features if feature.Name == name]
        if not matching_features:
            raise ValueError(f"{name} not found.")
        return matching_features

    @staticmethod
    def curves(name: Optional[str] = None) -> List[Curve]:
        all_collection : NXOpen.CurveCollection = Part.work_part().Curves
        all_curves = []
        for one_curve in all_collection:
            all_curves.append(Curve(one_curve))
        if name is None:
            return all_curves
        matching_curves = [curve for curve in all_curves if curve.Name == name]
        if not matching_curves:
            raise ValueError(f"{name} not found.")
        return matching_curves

    @staticmethod
    def datum_planes(name: Optional[str] = None) -> List[DatumPlane]:
        datum_coll : NXOpen.DatumCollection = Part.work_part().Datums
        allDatumPlanes = []
        for one_datum_plane in datum_coll:
            if isinstance(one_datum_plane, NXOpen.DatumPlane):
                allDatumPlanes.append(DatumPlane(one_datum_plane))
        if name is None:
            return allDatumPlanes
        matching_planes = [plane for plane in allDatumPlanes if plane.Name == name]
        if not matching_planes:
            raise ValueError(f"{name} not found.")
        return matching_planes

    @staticmethod
    def datum_csys(name: Optional[str] = None) -> List[CoordinateSystem]:
        datum_csys : NXOpen.CoordinateSystem = Part.work_part().CoordinateSystems
        allDatumCsys = []
        for one_datum_csys in datum_csys:
            allDatumCsys.append(CoordinateSystem(one_datum_csys))
        if name is None:
            return allDatumCsys
        matching_csys = [csys for csys in allDatumCsys if csys.Name == name]
        if not matching_csys:
            raise ValueError(f"{name} not found.")
        return matching_csys

    @staticmethod
    def datum_axes(name: Optional[str] = None) -> List[DatumAxis]:
        datum_coll : NXOpen.DatumCollection = Part.work_part().Datums
        all_datum_axes = []
        for one_datum_axis in datum_coll:
            if isinstance(one_datum_axis, NXOpen.DatumAxis):
                all_datum_axes.append(DatumAxis(one_datum_axis))
        if name is None:
            return all_datum_axes
        matching_axes = [axis for axis in all_datum_axes if axis.Name == name]
        if not matching_axes:
            raise ValueError(f"{name} not found.")
        return matching_axes
 
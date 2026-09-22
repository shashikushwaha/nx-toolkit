import sys
from .named_object import NamedObject
from .body import Body
from typing import List
import NXOpen
import NXOpen_Features


class Feature(NamedObject):
    def __init__(self, nxFeature: NXOpen_Features.Feature):
        super().__init__(nxFeature)

    @property
    def nx_object(self) -> NXOpen_Features.Feature:
        return super().nx_object

    @staticmethod
    def Boolean(targetBody : Body, toolBodies : List[Body]) -> "Feature":
        theSession : NXOpen.Session  = NXOpen.Session.GetSession()
        workPart : NXOpen.Part = theSession.Parts.Work
        booleanBuilder1: NXOpen_Features.BooleanBuilder = workPart.Features.CreateBooleanBuilderUsingCollector(NXOpen_Features.BooleanFeature.Null)
        scCollector1 : NXOpen.ScCollector = booleanBuilder1.ToolBodyCollector        
        booleanRegionSelect1  = booleanBuilder1.BooleanRegionSelect        
        booleanBuilder1.Tolerance = 0.001        
        booleanBuilder1.Operation = NXOpen_Features.Feature.BooleanType.Unite
        added1 = booleanBuilder1.Targets.Add(targetBody)        
        targets1 = [NXOpen.TaggedObject.Null] * 1 
        targets1[0] = targetBody.nx_object
        booleanRegionSelect1.AssignTargets(targets1)        
        scCollector2 = workPart.ScCollectors.CreateCollector()        
        bodies1 = [NXOpen.Body.Null] * 1 
        body2 = workPart.Bodies.FindObject("BLOCK(3)")
        bodies1[0] = body2
        bodyDumbRule1 = workPart.ScRuleFactory.CreateRuleBodyDumb(toolBodies, True)
        
        rules1 = [None] * 1 
        rules1[0] = bodyDumbRule1
        scCollector2.ReplaceRules(rules1, False)
        booleanBuilder1.ToolBodyCollector = scCollector2       
        nXObject1 = booleanBuilder1.Commit()        
        booleanBuilder1.Destroy() 
        return nXObject1       

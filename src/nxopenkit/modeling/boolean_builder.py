import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
import math
from typing import List, Optional
from .feature_builder import FeatureBuilder
from  nxopenkit.core import Body, Part, Feature



class BooleanBuilder(FeatureBuilder):
    def __init__(self, target_body: Body, tool_bodies : List[Body], boolean_type : Optional[NXOpen.Features.Feature.BooleanType] = NXOpen.Features.Feature.BooleanType.Unite):
        self.target_body = target_body
        self.tool_bodies = tool_bodies
        self.boolean_type = boolean_type
        super().__init__(self)
        workPart : NXOpen.Part = Part.work_part()
        booleanBuilder1: NXOpen.Feature.BooleanBuilder = workPart.Features.CreateBooleanBuilderUsingCollector(NXOpen.Features.BooleanFeature.Null)
        self.feature_builder = booleanBuilder1
        scCollector1 : NXOpen.ScCollector = booleanBuilder1.ToolBodyCollector        
        booleanRegionSelect1  = booleanBuilder1.BooleanRegionSelect        
        booleanBuilder1.Tolerance = self.distance_tolerance        
        booleanBuilder1.Operation = self.boolean_type
        added1 = booleanBuilder1.Targets.Add(self.target_body)             
        targets1 = [NXOpen.TaggedObject.Null] * 1 
        targets1[0] = target_body.nx_object
        booleanRegionSelect1.AssignTargets(targets1)        
        scCollector2 = workPart.ScCollectors.CreateCollector()        
        bodies1 = [NXOpen.Body.Null] * 1 
        body2 = workPart.Bodies.FindObject("BLOCK(3)")
        bodies1[0] = body2
        bodyDumbRule1 = workPart.ScRuleFactory.CreateRuleBodyDumb(tool_bodies, True)
        
        rules1 = [None] * 1 
        rules1[0] = bodyDumbRule1
        scCollector2.ReplaceRules(rules1, False)
        booleanBuilder1.ToolBodyCollector = scCollector2       
        # nXObject1 = booleanBuilder1.Commit()        
        # booleanBuilder1.Destroy() 
        # return nXObject1       

import NXOpen
# import NXOpen.Features
from .builder import Builder
from nxopenkit import Feature


class FeatureBuilder(Builder) : 
    def __init__(self):
        self.feature_builder : NXOpen.Features.FeatureBuilder = None        
        super().__init__()
        self.builder = self.feature_builder

    def commit_feature(self) -> Feature:
        should_destroy = True
        try:
            feature = self.feature_builder.CommitFeature()
            if feature is None:
                raise ValueError("CommitFeature returned no feature")
            return Feature(feature)
        except NXOpen.NXException as error:
            self.undo_mark()
            should_destroy = False
            raise ValueError(error.Message) from error
        finally:
            if should_destroy:
                self.destroy()



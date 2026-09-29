import NXOpen
import NXOpen.Features
from .base_builder import BaseBuilder


class FeatureBuilder(BaseBuilder):
    def __init__(self):
        self.feature_builder : NXOpen.Features.FeatureBuilder = None
        self.builder = self.feature_builder
        super().__init__(self)

    def commit_feature(self):
        should_destroy = True
        try:
            feature = self.feature_builder.CommitFeature()
            if feature is None:
                raise ValueError("CommitFeature returned no feature")
            return feature
        except NXOpen.NXException as error:
            self.undo_mark()
            should_destroy = False
            raise ValueError(error.Message) from error
        finally:
            if should_destroy:
                self.destroy()



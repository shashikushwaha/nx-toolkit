from __future__ import annotations

from nxopenkit.core.point import Point
from .named_object import NamedObject
from typing import List, cast
import NXOpen
import NXOpen.Features


class Feature(NamedObject):
    def __init__(self, nxFeature: NXOpen.Features.Feature):
        super().__init__(nxFeature)

    @property
    def to_nx(self) -> NXOpen.Features.Feature:
        return cast(NXOpen.Features.Feature, super().to_nx)

    @property
    def get_points(self) -> List[Point]:
        return [Point(one_point) for one_point in self.to_nx.GetEntities() if isinstance(one_point, NXOpen.Point)]
        
        

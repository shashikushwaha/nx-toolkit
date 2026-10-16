from __future__ import annotations

from typing import Sequence, Union

import NXOpen
from nxopenkit.core.tagged_object import TaggedObject

from dataclasses import dataclass
from nxopenkit.core.types import Double
from nxopenkit.maths.point3d import Point3d
from nxopenkit.core.session import Session

@dataclass(frozen=True)
class MinimumDistanceResult:
    distance: float
    point_on_source: Point3d
    point_on_destination: Point3d

@dataclass
class ClosestObjectResult:
    distance : float
    source_object: object
    destination_object : object
    point_on_source : Point3d
    point_on_destination: Point3d

class Measurement:

    @staticmethod
    def get_minimum_dist(
        source: Union[TaggedObject, Point3d],
        destination: Union[TaggedObject, Point3d],
    ) -> MinimumDistanceResult:

        if isinstance(source, TaggedObject):
            tag1 = source.tag
            guess1_given = 0
            guess1 = [0.0, 0.0, 0.0]
        else:
            tag1 = 0
            guess1_given = 1
            guess1 = source.to_array

        if isinstance(destination, TaggedObject):
            tag2 = destination.tag
            guess2_given = 0
            guess2 = [0.0, 0.0, 0.0]
        else:
            tag2 = 0
            guess2_given = 1
            guess2 = destination.to_array

        dist, pt1, pt2 = Session.uf_session().Modeling.AskMinimumDist(
            tag1,
            tag2,
            guess1_given,
            guess1,
            guess2_given,
            guess2,
        )

        return MinimumDistanceResult(
            distance=float(dist),
            point_on_source=Point3d(*pt1),
            point_on_destination=Point3d(*pt2),
        )


    @staticmethod
    def get_closest_object(
        source: TaggedObject,
        candidates: Sequence[TaggedObject],
    ) -> ClosestObjectResult:

        uf = NXOpen.UF.UFSession.GetUFSession()

        closest_obj = None
        point_on_source = None
        point_on_destination = None
        min_distance = float("inf")
        for candidate in candidates:

            if candidate.Tag == source.Tag:
                continue

            distance_result = Measurement.get_minimum_dist(source.Tag, candidate.Tag)
            if distance_result.distance < min_distance:
                min_distance = distance_result.distance
                closest_obj = candidate
                point_on_destination = distance_result.point_on_destination
                point_on_source = distance_result.point_on_source

        return ClosestObjectResult(
            distance=min_distance,
            source_object=source,
            destination_object= closest_obj,
            point_on_source=point_on_source,
            point_on_destination=point_on_destination,
            object=closest_obj,
            
        )

    @staticmethod
    def get_closest_pair(
        sources: Sequence[TaggedObject],
        candidates: Sequence[TaggedObject],
    ) -> ClosestObjectResult:

        closest_source = None
        closest_destination = None
        point_on_source = None
        point_on_destination = None
        min_distance = float("inf")

        for source in sources:
            for candidate in candidates:

                if source.tag == candidate.tag:
                    continue

                distance_result = Measurement.get_minimum_dist(
                    source,
                    candidate,
                )

                if distance_result.distance < min_distance:
                    min_distance = distance_result.distance
                    closest_source = source
                    closest_destination = candidate
                    point_on_source = distance_result.point_on_source
                    point_on_destination = distance_result.point_on_destination

        return ClosestObjectResult(
            distance=min_distance,
            source_object=closest_source,
            destination_object=closest_destination,
            point_on_source=point_on_source,
            point_on_destination=point_on_destination,
            object=closest_destination,
        )
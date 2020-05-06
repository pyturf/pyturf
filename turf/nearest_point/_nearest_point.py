from typing import Dict, List, Sequence, TypeVar, Union
from copy import deepcopy

from turf.distance import distance
from turf.explode import explode
from turf.helpers import point, Point
from turf.helpers import Feature, FeatureCollection, Geometry
from turf.invariant import get_coords_from_features


GeoJson = TypeVar("GeoJson", Dict, Feature, FeatureCollection, Geometry)


def nearest_point(target: Union[Sequence, Dict, Feature], features: GeoJson) -> Point:
    """
    Calculates the closest reference point from a feature collection towards a target point
    This calculation is geodesic.

    :param target: targetPoint the reference point
    :param features: points against input point set
    :return: the closest point in the features set to the reference point
    """
    min_distance = float("inf")
    nearest_point = None
    feature_index = None

    features = explode(features)
    points = features.get("features")

    target = get_coords_from_features(target, ["Point"])

    for i, point in enumerate(points):
        dist = distance(target, point)
        if dist < min_distance:
            min_distance = dist
            nearest_point = deepcopy(point)
            feature_index = i

    if "properties" in nearest_point:
        nearest_point["properties"].update(
            {"featureIndex": feature_index, "distanceToPoint": min_distance}
        )
    else:
        nearest_point.update(
            {
                "properties": {
                    "featureIndex": feature_index,
                    "distanceToPoint": min_distance,
                }
            }
        )

    return nearest_point

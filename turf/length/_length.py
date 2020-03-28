from functools import reduce

from turf.distance import distance
from turf.invariant import get_coords_from_features


def length(features, options=None):
    """
    Calculates the total length of the input Feature / FeatureCollection in the specified units.

    :param features: a Feature / FeatureCollection of types LineString, MultiLineString, Polygon or MultiPolygon
    :param options: optional parameters
        [options["units"]=kilometers] can be degrees, radians, miles, or kilometers
    :return: the measured distance
    """

    coords = get_coords_from_features(
        features, ["LineString", "MultiLineString", "Polygon", "MultiPolygon",]
    )

    if any(isinstance(inner_item, list) for item in coords for inner_item in item):
        distances = list(map(lambda sub_item: length(sub_item, options), coords))
        return sum(distances)

    total_distance = reduce(
        lambda accum, coord: accum + distance(coord[0], coord[1], options),
        zip(coords, coords[1:]),
        0,
    )

    return total_distance

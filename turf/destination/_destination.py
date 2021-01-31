from math import asin, atan2, cos, sin

from turf.helpers import (
    degrees_to_radians,
    length_to_radians,
    radians_to_degrees,
    point,
)
from turf.invariant import get_coords_from_features
from turf.utils.helpers import truncate


def destination(origin, distance, bearing, options=None):
    """
    Takes a Point and calculates the location of a destination point given a distance in
    degrees, radians, miles, or kilometers; and bearing in degrees.
    This uses the [Haversine formula](http://en.wikipedia.org/wiki/Haversine_formula) to account for global curvature.

    :param origin: starting point
    :param distance: distance from the origin point
    :param bearing: bearing ranging from -180 to 180
    :param options: optional parameters
        [options["units"]='kilometers'] miles, kilometers, degrees, or radians
        [options["properties"]={}] Translate properties to Point
    :return: destination GeoJSON Point feature
    """

    if not options:
        options = {}

    kwargs = {}
    if "units" in options:
        kwargs["units"] = options.get("units")

    coords = get_coords_from_features(origin, ["Point"])

    longitude1 = degrees_to_radians(coords[0])
    latitude1 = degrees_to_radians(coords[1])
    bearing_rads = degrees_to_radians(bearing)

    radians = length_to_radians(distance, **kwargs)

    latitude2 = asin(
        sin(latitude1) * cos(radians)
        + cos(latitude1) * sin(radians) * cos(bearing_rads)
    )

    longitude2 = longitude1 + atan2(
        sin(bearing_rads) * sin(radians) * cos(latitude1),
        cos(radians) - sin(latitude1) * sin(latitude2),
    )

    lng = truncate(radians_to_degrees(longitude2), 6)
    lat = truncate(radians_to_degrees(latitude2), 6)

    return point([lng, lat], options.get("properties", None))

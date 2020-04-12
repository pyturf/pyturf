import numpy as np
from turf.helpers import degrees_to_radians, radians_to_length
from turf.invariant import get_coords_from_features


def distance(start, end, options=None):
    """
    Calculates the distance between two Points in degrees, radians, miles, or kilometers.
    This uses the [Haversine formula](http://en.wikipedia.org/wiki/Haversine_formula) to account for global curvature.

    :param start: starting point [lng, lat] or Point feature
    :param end: ending point [lng, lat] or Point feature
    :param options: dictionary with units as an attribute. Can be degrees, radians, miles, or kilometers
    :return: distance between the 2 points
    """

    kwargs = {}
    if isinstance(options, dict) and "units" in options:
        kwargs.update(options)

    coordinates1 = get_coords_from_features(start, ["Point"])
    coordinates2 = get_coords_from_features(end, ["Point"])

    d_lat = degrees_to_radians(coordinates2[1] - coordinates1[1])
    d_lon = degrees_to_radians(coordinates2[0] - coordinates1[0])

    lat1 = degrees_to_radians(coordinates1[1])
    lat2 = degrees_to_radians(coordinates2[1])

    distance_rad = calculate_radians_distance(d_lon, d_lat, lat1, lat2)

    return radians_to_length(distance_rad, **kwargs)


def calculate_radians_distance(dif_lon, dif_lat, lat1, lat2):
    """
    Calculates the distance between start and end

    basic haversine formula
    http://www.edwilliams.org/avform.htm#Dist
    https://en.wikipedia.org/wiki/Great-circle_distance

    :param dif_lon: longitudinal difference (radians) between start and ending points
    :param dif_lat: latitudinal difference (radians) between start and ending points
    :param lat1: radians latitude for starting point
    :param lat2: radians latitude for ending point

    :return: distance_radians
    """
    d = np.sin(dif_lat / 2) ** 2 + np.sin(dif_lon / 2) ** 2 * np.cos(lat1) * np.cos(
        lat2
    )
    d = 2 * np.arctan2(np.sqrt(d), np.sqrt(1 - d))

    return d

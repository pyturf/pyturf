import numpy as np
from turf.helpers import degrees_to_radians, radians_to_length
from turf.invariant import get_coord


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

    coordinates1 = get_coord(start)
    coordinates2 = get_coord(end)

    d_lat = degrees_to_radians(coordinates2[1] - coordinates1[1])
    d_lon = degrees_to_radians(coordinates2[0] - coordinates1[0])

    lat1 = degrees_to_radians(coordinates1[1])
    lat2 = degrees_to_radians(coordinates2[1])

    a = np.sin(d_lat / 2) ** 2 + np.sin(d_lon / 2) ** 2 * np.cos(lat1) * np.cos(lat2)

    return radians_to_length(2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)), **kwargs)

import numpy as np

from turf.invariant import get_coords_from_features
from turf.helpers import degrees_to_radians, radians_to_degrees


def bearing(start, end, options=None):
    """
    Takes two points and finds the geographic bearing between them,
    i.e. the angle measured in degrees from the north line (0 degrees)

    :param start: starting point [lng, lat] or Point feature
    :param end: ending point [lng, lat] or Point feature
    :param options: dictionary with options:
        [options["final"]] - calculates the final bearing if true
    :return: bearing in decimal degrees, between -180 and 180 (positive clockwise)
    """

    if not options:
        options = {}

    if isinstance(options, dict) and "final" in options:
        return calculate_final_bearing(start, end)

    start = get_coords_from_features(start, ["Point"])
    end = get_coords_from_features(end, ["Point"])

    lon1 = degrees_to_radians(start[0])
    lon2 = degrees_to_radians(end[0])
    lat1 = degrees_to_radians(start[1])
    lat2 = degrees_to_radians(end[1])

    a = np.sin(lon2 - lon1) * np.cos(lat2)

    b = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lon2 - lon1)

    return radians_to_degrees(np.arctan2(a, b))


def calculate_final_bearing(start, end):
    bear = bearing(end, start)
    return (bear + 180) % 360

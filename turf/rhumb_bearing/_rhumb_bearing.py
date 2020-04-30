from math import fmod
from typing import Dict, Sequence, Union

import numpy as np

from turf.helpers import degrees_to_radians, radians_to_degrees
from turf.helpers import Feature
from turf.invariant import get_coords_from_features


def rhumb_bearing(
    origin: Union[Sequence, Dict, Feature],
    destination: Union[Sequence, Dict, Feature],
    options: Dict = None,
) -> float:
    """
    Takes two {Point|points} and finds the bearing angle between them along a
    Rhumb line
    * i.e. the angle measured in degrees start the north line (0 degrees)

    https://en.wikipedia.org/wiki/Rhumb_line

    :param start: starting point [lng, lat] or Point feature
    :param end: ending point [lng, lat] or Point feature
    :param options: Optional parameters
        [options["final"]]: Calculates the final bearing if True

    :return: bearing from north in decimal degrees
    """
    if not isinstance(options, dict):
        options = {}

    origin = get_coords_from_features(origin, ["Point"])
    destination = get_coords_from_features(destination, ["Point"])
    final = options.get("final", False)

    if final:
        bearing = calculate_rhumb_bearing(destination, origin)
    else:
        bearing = calculate_rhumb_bearing(origin, destination)

    return bearing


def calculate_rhumb_bearing(origin: Sequence, destination: Sequence) -> float:
    """
    Calculates the bearing from origin to destination point along a rhumb line.
    http://www.edwilliams.org/avform.htm#Rhumb
    """
    phi_1 = degrees_to_radians(origin[1])
    phi_2 = degrees_to_radians(destination[1])
    delta_lambda = degrees_to_radians(destination[0] - origin[0])

    # if delta_lambda over 180° take shorter rhumb line across the anti-meridian:
    if abs(delta_lambda) > np.pi:
        if delta_lambda > 0:
            delta_lambda = -(2 * np.pi - delta_lambda)
        if delta_lambda < 0:
            delta_lambda = 2 * np.pi + delta_lambda

    delta_psi = np.log(np.tan(phi_2 / 2 + np.pi / 4) / np.tan(phi_1 / 2 + np.pi / 4))
    theta = np.arctan2(delta_lambda, delta_psi)

    return fmod(radians_to_degrees(theta) + 360, 360)

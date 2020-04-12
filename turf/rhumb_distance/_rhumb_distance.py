from typing import Dict, List

import numpy as np

from turf.helpers import convert_length, degrees_to_radians
from turf.helpers import earth_radius
from turf.invariant import get_coords_from_features


def rhumb_distance(origin, destination, options: Dict = None) -> float:
    """
    Calculates the rhumb distance between two Points. Units are defined in helpers._units

    # https://en.wikipedia.org/wiki/Rhumb_line

    :param start: starting point [lng, lat] or Point feature
    :param end: ending point [lng, lat] or Point feature
    :param options: dictionary with units as an attribute.
                    Units are defined in helpers._units

    :return: distance between the 2 points

    """
    if not isinstance(options, dict):
        options = {}

    origin = get_coords_from_features(origin, ["Point"])
    destination = get_coords_from_features(destination, ["Point"])

    # compensate the crossing of the 180th meridian (https://macwright.org/2016/09/26/the-180th-meridian.html)
    # solution from https://github.com/mapbox/mapbox-gl-js/issues/3250#issuecomment-294887678
    if (destination[0] - origin[0]) > 180:
        destination[0] -= 360
    elif (origin[0] - destination[0]) > 180:
        destination[0] += 360

    distance_in_meters = calculate_rhumb_distance(origin, destination)

    distance = convert_length(
        distance_in_meters, "meters", options.get("units", "kilometers")
    )

    return distance


def calculate_rhumb_distance(
    origin: List, destination: List, radius: float = None
) -> float:
    """
    Calculates the rhumb distance between two Points.

    # https://en.wikipedia.org/wiki/Rhumb_line

    :param origin: starting point [lng, lat]
    :param destination: ending point [lng, lat]
    :param radius: radius of the earth

    :return: distance between the 2 points in meters
    """
    if not radius:
        radius = earth_radius

    phi_1 = degrees_to_radians(origin[1])
    phi_2 = degrees_to_radians(destination[1])
    delta_phi = phi_2 - phi_1

    delta_lambda = degrees_to_radians(abs(destination[0] - origin[0]))

    # if dLon over 180° take shorter rhumb line across the anti-meridian:
    if delta_lambda > np.pi:
        delta_lambda -= 2 * np.pi

    # on Mercator projection, longitude distances shrink by latitude; q is the 'stretch factor'
    # q becomes ill-conditioned along E-W line (0/0); use empirical tolerance to avoid it

    delta_psi = np.log(np.tan(phi_2 / 2 + np.pi / 4) / np.tan(phi_1 / 2 + np.pi / 4))

    if abs(delta_psi) > 10e-12:
        q_1 = delta_phi / delta_psi
    else:
        q_1 = np.cos(phi_1)

    # distance is pythagoras on 'stretched' Mercator projection
    delta = np.sqrt(delta_phi * delta_phi + q_1 * q_1 * delta_lambda * delta_lambda)
    # angular distance in radians
    distance = delta * radius

    return distance

from math import fmod
from typing import Dict, List, Sequence, Union

import numpy as np

from turf.helpers import convert_length, degrees_to_radians
from turf.helpers import earth_radius
from turf.helpers import point, Point
from turf.invariant import get_coords_from_features


def rhumb_destination(features: Dict, options: Dict = None) -> Point:
    """
    Returns the destination {Point} having travelled the given distance along a
    Rhumb line from the origin Point with the (varant) given bearing.

    # https://en.wikipedia.org/wiki/Rhumb_line

    :param features: any GeoJSON feature or feature collection
    :param properties: specification to calculate the rhumb line
        [options["distance"]=100] distance from the starting point
        [options["bearing"]=180] varant bearing angle ranging from -180 to 180 degrees from north
        [options["units"]=kilometers] units: specifies distance (can be degrees, radians, miles, or kilometers)

    :param options: optional parameters also be part of features["properties"]
        [options["units"]={}] can be degrees, radians, miles, or kilometers
        [options["properties"]={}] Translate GeoJSON Properties to Point
        [options["id"]={}] Translate GeoJSON Id to Point

    :return: a FeatureDestination point.
    """
    if not options:
        options = features.get("properties", {})

    coords = get_coords_from_features(features, ["Point"])

    bearing = options.get("bearing", 180)
    distance = options.get("dist", 100)
    units = options.get("units", "kilometers")

    distance_in_meters = convert_length(
        abs(distance), original_unit=units, final_unit="meters"
    )

    if distance < 0:
        distance_in_meters *= -1

    destination = calculate_rhumb_destination(coords, distance_in_meters, bearing)

    # compensate the crossing of the 180th meridian:
    #  (https://macwright.org/2016/09/26/the-180th-meridian.html)
    # solution from:
    # https://github.com/mapbox/mapbox-gl-js/issues/3250#issuecomment-294887678

    if (destination[0] - coords[0]) > 180:
        destination[0] -= 360
    elif (coords[0] - destination[0]) > 180:
        destination[0] += 360

    return point(destination, options.get("properties", None))


def calculate_rhumb_destination(
    origin: Sequence, distance_in_meters: float, bearing: float, radius: float = None
) -> List:
    """
    Calculates the destination point having travelled along a rhumb line
    from origin point the given distance on the  given bearing.
    Adapted from Geodesy:
    http://www.movable-type.co.uk/scripts/latlong.html#rhumblines

    param origin: point coordinates in [lng, lat] form
    param distance: - Distance travelled, in same units as earth radius (default: metres).
    param bearing: - Bearing in degrees from north.
    param radius: - (Mean) radius of earth

    returns destination: point.
    """
    if not radius:
        radius = earth_radius

    # angular distance in radians
    delta = distance_in_meters / radius
    # to radians, but without normalize to pi
    lambda_1 = origin[0] * np.pi / 180

    phi_1 = degrees_to_radians(origin[1])
    theta = degrees_to_radians(bearing)

    delta_phi = delta * np.cos(theta)
    phi_2 = phi_1 + delta_phi

    # check for some points going past the pole, normalise latitude if so
    if abs(phi_2) > (np.pi / 2) and (phi_2 > 0):
        phi_2 = np.pi - phi_2
    if abs(phi_2) > (np.pi / 2) and (phi_2 < 0):
        phi_2 = np.pi - phi_2

    delta_psi = np.log(np.tan(phi_2 / 2 + np.pi / 4) / np.tan(phi_1 / 2 + np.pi / 4))

    # E-W course becomes ill-conditioned with 0/0
    if abs(delta_psi) > 10e-12:
        q_1 = delta_phi / delta_psi
    else:
        q_1 = np.cos(phi_1)

    delta_lambda = delta * np.sin(theta) / q_1
    lambda_2 = lambda_1 + delta_lambda

    # normalise to −180..+180°
    destination = [
        fmod(((lambda_2 * 180 / np.pi) + 540), 360) - 180,
        (phi_2 * 180 / np.pi),
    ]

    return destination

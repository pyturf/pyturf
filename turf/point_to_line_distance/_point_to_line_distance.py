from typing import Dict, List, Sequence, Union

import numpy as np

from turf.distance import distance
from turf.rhumb_distance import rhumb_distance
from turf.helpers import convert_length, Feature
from turf.invariant import get_coords_from_features


def point_to_line_distance(
    point: Union[Sequence, Dict, Feature],
    line: Union[Sequence, Dict, Feature],
    options: Dict = None,
) -> float:
    """
    Returns the minimum distance between a {Point} and a {LineString},
    being the distance from a line the minimum distance between the point and
    any segment of the `LineString`

    http://geomalgorithms.com/a02-_lines.html

    :param point: Point GeoJSON Feature or Geometry
    :param line: LineString GeoJSON Feature or Geometry
    :param options: Optional parameters
        [options["units"]]: any supported unit (e.g. degrees, radians, miles...)
        [options["method"]]: geodesic or 'planar for distance calculation

    :return: distance between point and line
    """
    dist = []
    if not isinstance(options, dict):
        options = {"method": "geodesic", "units": "kilometers"}

    point = get_coords_from_features(point, ["Point"])
    line = get_coords_from_features(line, ["LineString"])

    for i in range(1, len(line)):
        dist.append(
            get_distance_to_segment(
                point, line[i - 1], line[i], options.get("method", "geodesic")
            )
        )

    dist = convert_length(min(dist), "degrees", options.get("units", "kilometers"))

    return dist


def get_distance_to_segment(
    point: List, segment_start: List, segment_end: List, method: str
):
    """
    Calculates the distance from the point to the segment.

    :param point: Point coordinates
    :param segment_start: segment start point from the line feature
    :param segment_end: adjacent segment end point from the line feature
    :param method: wether to calculate the distance based on geodesic
                    (spheroid) or planar (flat) method.
                          Valid options are: 'geodesic' or 'planar

    :return: distance between point and both segments"""
    v = [segment_end[0] - segment_start[0], segment_end[1] - segment_start[1]]

    w = [point[0] - segment_start[0], point[1] - segment_start[1]]

    c1 = np.dot(w, v)
    c2 = np.dot(v, v)

    b2 = c1 / c2
    point_2 = [segment_start[0] + (b2 * v[0]), segment_start[1] + (b2 * v[1])]

    if c1 <= 0:
        dist = calculate_distance_by_method(point, segment_start, method)
    elif c2 <= c1:
        dist = calculate_distance_by_method(point, segment_end, method)
    else:
        dist = calculate_distance_by_method(point, point_2, method)

    return dist


def calculate_distance_by_method(point_1: List, point_2: List, method: str) -> float:
    """
    Wrapper to calculate the distance between two points. Depending on the
    method, if calls rhumb distance or haversine distance

    :param point_1: Point coordinates
    :param point_2: Point coordinates
    :param method: wether to calculate the distance based on geodesic
                          (spheroid) or planar (flat) method.
                          Valid options are: 'geodesic' or 'planar

    :return: distance between point and both segments in radians
    """

    if method == "planar":
        dist = rhumb_distance(point_1, point_2, {"units": "degrees"})
    else:
        dist = distance(point_1, point_2, {"units": "degrees"})

    return dist

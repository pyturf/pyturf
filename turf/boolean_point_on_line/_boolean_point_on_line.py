from typing import Dict, List, Sequence, TypeVar, Union
from decimal import Decimal, getcontext
from math import sqrt

from turf.helpers import Feature, LineString, Point
from turf.helpers import feature_collection, line_string, multi_line_string
from turf.invariant import get_coords_from_features


ctx = getcontext()
ctx.prec = 28

PointFeature = TypeVar("PointFeature", Dict, Feature, Point)
LineFeature = TypeVar("LineFeature", Dict, Feature, LineString)


def boolean_point_on_line(
    point: PointFeature, line: LineFeature, options: Dict = {}
) -> bool:
    """
    Returns True if a point is on a line else False.
    Accepts a optional parameter to ignore the start and end vertices of the linestring.

    :param point: {Point} GeoJSON Point
    :param line: {LineString} GeoJSON LineString
    :param options: Optional parameters
        [options["ignoreEndVertices"]=False] whether to ignore the start and end vertices

    :return: boolean True/False if point is on line
    """
    if not isinstance(options, dict):
        options = {}

    point_on_line = False

    ignore_end_vertices = options.get("ignoreEndVertices", False)

    point_coord = get_coords_from_features(point, ("Point",))
    line_coords = get_coords_from_features(line, ("LineString",))

    for i in range(len(line_coords) - 1):
        if ignore_end_vertices:
            # ignore if point_coord are the line start
            if (i == 0) and (point_coord == line_coords[i]):
                continue

            # ignore if point_coord are the line end
            if ((i + 1) == (len(line_coords) - 1)) and (
                point_coord == line_coords[i + 1]
            ):
                continue

        point_on_line = point_on_segment(
            point_coord, line_coords[i], line_coords[i + 1]
        )

        if point_on_line:
            break

    return point_on_line


def point_on_segment(
    point: List, segment_start: List, segment_end: List, epsilon: float = 1.0e-14
) -> bool:
    """
    Checks if a given point is on a line or not.

    Since this is a comparison of floats, I use the Decimal module of python


    :param point: Coordinates of a point
    :param segment_start: Coordinates of the start line
    :param segment_end: Coordinates of the line end
    :return: bool
    """

    len_segment = Decimal(
        sqrt(
            pow(segment_end[0] - segment_start[0], 2)
            + pow(segment_end[1] - segment_start[1], 2)
        )
    )

    len_point_seg_1 = Decimal(
        sqrt(pow(point[0] - segment_start[0], 2) + pow(point[1] - segment_start[1], 2))
    )

    len_point_seg_2 = Decimal(
        sqrt(pow(segment_end[0] - point[0], 2) + pow(segment_end[1] - point[1], 2))
    )

    return abs(len_segment - len_point_seg_1 - len_point_seg_2) <= epsilon

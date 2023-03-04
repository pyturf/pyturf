from typing import Dict, Sequence, TypeVar, Union
from collections import deque

from rtree import index

from turf.helpers import (
    Feature,
    FeatureCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
    get_input_dimensions,
)

from turf.envelope._envelope import envelope
from turf.polygon_to_line import polygon_to_line
from turf.helpers import feature, feature_collection, line_string, point
from turf.invariant import get_coords_from_features, get_geometry_type
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


LinePolyFeature = TypeVar(
    "LineFeature",
    Dict,
    Feature,
    FeatureCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Polygon,
)


def line_intersect(input_1: LinePolyFeature, input_2: LinePolyFeature) -> Feature:
    """
    Takes any LineString or Polygon GeoJSON and returns the intersecting point(s).

    :param line_1: {GeoJSON} line1 any LineString or Polygon
    :param line_2:{GeoJSON} line2 any LineString or Polygon
    :returns: {FeatureCollection<Point>} point(s) that intersect both
    """
    line_1_segments = get_line_segments(input_1)
    line_2_segments = get_line_segments(input_2)

    possible_intersects = []
    intersects = []

    possible_intersects.extend(spatial_filtering(line_1_segments, line_2_segments))

    for i in possible_intersects:
        pnt = calculate_intersect(*i)

        if pnt:
            intersects.append(pnt)

    return feature_collection(intersects)


def spatial_filtering(line_1: Sequence, line_2: Sequence) -> Sequence:
    """
    Filters possible intersections of the lines via their bounding box

    :param line_1: line_1 coordinates of segments
    :param line_2: line_2 coordinates of segments
    :returns: list of line segments that possibly intersect with each other
    """
    possible_intersects = []
    rtree_index = index.Index()

    for i, seg in enumerate(line_1):
        bbox = envelope(seg)
        rtree_index.insert(i, bbox["bbox"])

    for j, seg in enumerate(line_2):
        bbox = envelope(seg)
        seg_intersection_idx = deque(rtree_index.intersection(bbox["bbox"]))

        while seg_intersection_idx:
            seg_idx = seg_intersection_idx.pop()

            possible_intersects.append([*line_1[seg_idx], *line_2[j]])

    return possible_intersects


def calculate_intersect(
    seg_1_start: Sequence,
    seg_1_end: Sequence,
    seg_2_start: Sequence,
    seg_2_end: Sequence,
) -> Union[None, Point]:
    """
    Calculates the intersection point of two segments otherwise None

    :param seg_1_start: coordinates of segment 1 start
    :param seg_1_end: coordinates of segment 1 end
    :param seg_2_start: coordinates of segment 2 start
    :param seg_2_end: coordinates of segment 2 end
    :returns: {Point} if intersection, otherwise None
    """
    x1 = seg_1_start[0]
    y1 = seg_1_start[1]
    x2 = seg_1_end[0]
    y2 = seg_1_end[1]
    x3 = seg_2_start[0]
    y3 = seg_2_start[1]
    x4 = seg_2_end[0]
    y4 = seg_2_end[1]

    pnt = None

    denom = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))
    numeA = ((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))
    numeB = ((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))

    if denom == 0:
        return pnt

    uA = numeA / denom
    uB = numeB / denom

    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        x = round(x1 + (uA * (x2 - x1)), 6)
        y = round(y1 + (uA * (y2 - y1)), 6)
        pnt = point([x, y])

    return pnt


def get_line_segments(line: LinePolyFeature) -> Sequence:
    """
    Gets segments from a line feature

    :param line: any LineString or Polygon
    :return: sequence of segmetns
    """
    segments = []

    geometry_type = get_geometry_type(line)

    if isinstance(geometry_type, str):
        geometry_type = [geometry_type]

    for line_geo in geometry_type:
        if line_geo in ["MultiPolygon", "Polygon"]:
            line = polygon_to_line(line)
            line_geo = line["geometry"]["type"]

        line_coords = get_coords_from_features(line, ("LineString", "MultiLineString"))

        if line_geo in ["LineString"] and get_input_dimensions(line_coords) == 2:
            line_coords = [line_coords]

        for line_coord in line_coords:
            segments.extend(list(zip(line_coord, line_coord[1:])))

    return segments

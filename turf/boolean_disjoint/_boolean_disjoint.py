from typing import Any, List, Sequence, Union

from turf.helpers import (
    Feature,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
)

from turf.helpers import line_string, point, polygon

from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf.boolean_point_on_line import boolean_point_on_line
from turf.invariant import get_coords_from_features, get_geometry_type
from turf.polygon_to_line import polygon_to_line
from turf.line_intersect import line_intersect

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


def boolean_disjoint(feature_1: Any, feature_2: Any) -> bool:
    """
    Returns true if the intersection of the two geometries is an empty set.

    :param feature_1: {GeoJSON} feature_1 any Feature or Geometry
    :param feature_2: {GeoJSON} feature_2 any Feature or Geometry
    :return: boolean True/False if features are disjoint
    """
    is_disjoint = True

    flat_feature_1 = flatten_feature(feature_1)
    flat_feature_2 = flatten_feature(feature_2)

    for flat_1 in flat_feature_1:
        for flat_2 in flat_feature_2:
            is_disjoint = disjoint(flat_1, flat_2)

            if not is_disjoint:
                return is_disjoint

    return is_disjoint


def disjoint(
    feature_1: List[Union[str, Sequence]], feature_2: List[Union[str, Sequence]]
) -> bool:
    """
    Returns true if the intersection of the two geometries is an empty set.

    :param feature_1: {List} a List with geometry type and coordinates
    :param feature_2: {List} a List with geometry type and coordinates
    :return: boolean True/False if features are disjoint
    """
    is_disjoint = True

    if feature_1[0] in ["Point"]:
        if feature_2[0] in ["Point"]:
            is_disjoint = feature_1[1] != feature_2[1]

        elif feature_2[0] in ["LineString"]:
            is_disjoint = not boolean_point_on_line(feature_1[1], feature_2[1])

        elif feature_2[0] in ["Polygon"]:
            is_disjoint = not boolean_point_in_polygon(feature_1[1], feature_2[1])

    elif feature_1[0] in ["LineString"]:
        if feature_2[0] in ["Point"]:
            is_disjoint = not boolean_point_on_line(feature_2[1], feature_1[1])

        elif feature_2[0] in ["LineString"]:
            is_disjoint = not is_line_on_line(feature_1[1], feature_2[1])

        elif feature_2[0] in ["Polygon"]:
            is_disjoint = not is_line_in_poly(feature_2[1], feature_1[1])

    elif feature_1[0] in ["Polygon"]:
        if feature_2[0] in ["Point"]:
            is_disjoint = not boolean_point_in_polygon(feature_2[1], feature_1[1])

        elif feature_2[0] in ["LineString"]:
            is_disjoint = not is_line_in_poly(feature_1[1], feature_2[1])

        elif feature_2[0] in ["Polygon"]:
            is_disjoint = not is_poly_in_poly(feature_2[1], feature_1[1])

    return is_disjoint


def is_line_on_line(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if two linestring feature intersects each other

    :param feature_1: Coordinates of linestring feature 1
    :param feature_2: Coordinates of linestring feature 2
    :return: bool if there is an intersection
    """
    if isinstance(feature_1, list):
        feature_1 = line_string(feature_1)

    if isinstance(feature_2, list):
        feature_2 = line_string(feature_2)

    intersects = line_intersect(feature_1, feature_2)

    if len(intersects["features"]) >= 1:
        return True

    return False


def is_line_in_poly(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if a linestring feature is inside or intersects a polygon feature

    :param feature_1: Coordinates of polygon feature
    :param feature_2: Coordinates of linestring feature
    :return: bool if there is an intersection
    """
    feature_1_line = polygon_to_line(polygon(feature_1))

    if is_line_on_line(feature_2, feature_1_line):
        return True

    for coord in feature_2:
        if boolean_point_in_polygon(coord, feature_1):
            return True

    return False


def is_poly_in_poly(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if polygon feature_1 is inside polygon feature_2 and either way
    See http://stackoverflow.com/a/4833823/1979085

    :param feature: Coordinates of polygon feature 1
    :param feature: Coordinates of polygon feature 1
    :return: bool if there is an intersection
    """
    feature_1_line = polygon_to_line(polygon(feature_1))
    feature_2_line = polygon_to_line(polygon(feature_2))

    for coord1 in feature_1_line["geometry"]["coordinates"]:
        if boolean_point_in_polygon(coord1, feature_2):
            return True

    for coord2 in feature_2_line["geometry"]["coordinates"]:
        if boolean_point_in_polygon(coord2, feature_1):
            return True

    if is_line_on_line(feature_1_line, feature_2_line):
        return True

    return False


def flatten_feature(feature: Any) -> List[Union[str, Sequence]]:
    """
    Takes any feature and return the simple geometry type with coordinates.
    A MultiPoint will be flatten to Point, MultiLineString to LineString and
    MultiPolygon to Polygon

    :param feature: {GeoJSON} feature any Feature or Geometry
    :return: List of geometry type and coordinate sequence
    """
    feature_coords = get_coords_from_features(feature)
    feature_geometry = get_geometry_type(feature)

    if isinstance(feature_geometry, (list, tuple)):
        feature_geometry = feature_geometry[0]

    if feature_geometry in ["MultiPoint", "MultiLineString", "MultiPolygon"]:
        if feature_geometry == "MultiPoint":
            feature_geometry = "Point"

        elif feature_geometry == "MultiLineString":
            feature_geometry = "LineString"

        elif feature_geometry == "MultiPolygon":
            feature_geometry = "Polygon"

        flat_feature = [[feature_geometry, coords] for coords in feature_coords]

    else:
        flat_feature = [[feature_geometry, feature_coords]]

    return flat_feature

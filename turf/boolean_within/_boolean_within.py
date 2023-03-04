from typing import Any, List, Sequence, Union

from turf.helpers import point, polygon

from turf.bbox import bbox

# from turf.boolean_disjoint._boolean_disjoint import flatten_feature
from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf.boolean_point_on_line import boolean_point_on_line
from turf.invariant import get_coords_from_features, get_geometry_type
from turf.line_intersect import line_intersect
from turf.midpoint import midpoint
from turf.polygon_to_line import polygon_to_line


def boolean_within(feature_1: Any, feature_2: Any) -> bool:
    """
    Returns true if the first geometry is completely within the second geometry.

    The interiors of both geometries must intersect and, the interior and
    boundary of the primary (geometry a) must not intersect
    the exterior of the secondary (geometry b).

    :param feature_1: {GeoJSON} feature_1 any Feature or Geometry
    :param feature_2: {GeoJSON} feature_2 any Feature or Geometry

    :return: boolean True/False if feature 1 is within feature 2
    """
    feature_1 = get_features(feature_1)
    feature_2 = get_features(feature_2)

    return check_within(feature_1, feature_2)


def check_within(
    feature_1: List[Union[str, Sequence]], feature_2: List[Union[str, Sequence]]
) -> bool:
    """
    Returns true if the first geometry is completely within the second geometry

    :param feature_1: {List} a List with geometry type and coordinates
    :param feature_2: {List} a List with geometry type and coordinates

    :return: boolean True/False if feature 1 is within feature 2
    """
    is_within = False

    if feature_1[0] in ["Point"]:
        if feature_2[0] in ["Point", "MultiPoint"]:
            is_within = boolean_point_on_point(feature_1[1], feature_2[1])

        elif feature_2[0] in ["LineString", "MultiLineString"]:
            is_within = boolean_point_on_line(
                feature_1[1], feature_2[1], {"ignoreEndVertices": True}
            )

        elif feature_2[0] in ["Polygon", "MultiPolygon"]:
            is_within = boolean_point_in_polygon(
                feature_1[1], feature_2[1], {"ignoreBoundary": True}
            )

    if feature_1[0] in ["MultiPoint"]:
        if feature_2[0] in ["MultiPoint"]:
            is_within = all(
                boolean_point_on_point(coords_1, feature_2[1])
                for coords_1 in feature_1[1]
            )

        elif feature_2[0] in ["LineString", "MultiLineString"]:
            is_within = is_multipoint_on_linestring(feature_1, feature_2)

        elif feature_2[0] in ["Polygon", "MultiPolygon"]:
            is_within = is_multipoint_on_polygon(feature_1, feature_2)

    elif feature_1[0] in ["LineString"]:
        if feature_2[0] in ["LineString"]:
            is_within = is_line_on_line(feature_1[1], feature_2[1])

        if feature_2[0] in ["MultiLineString"]:
            is_within = is_line_on_multiline(feature_1[1], feature_2[1])

        elif feature_2[0] in ["Polygon"]:
            is_within = is_line_in_poly(feature_1[1], feature_2[1])

        elif feature_2[0] in ["MultiPolygon"]:
            is_within = is_line_in_multipoly(feature_1[1], feature_2[1])

    elif feature_1[0] in ["MultiLineString"]:
        if feature_2[0] in ["MultiLineString"]:
            is_within = all(
                is_line_on_multiline(coords_1, feature_2[1])
                for coords_1 in feature_1[1]
            )

        elif feature_2[0] in ["Polygon", "MultiPolygon"]:
            is_within = all(
                is_line_in_poly(coords_1, feature_2[1]) for coords_1 in feature_1[1]
            )

    elif feature_1[0] in ["Polygon"]:
        if feature_2[0] in ["Polygon"]:
            is_within = is_poly_in_poly(feature_1[1], feature_2[1])

        if feature_2[0] in ["MultiPolygon"]:
            is_within = is_poly_in_multipoly(feature_1[1], feature_2[1])

    elif feature_1[0] in ["MultiPolygon"]:
        if feature_2[0] in ["MultiPolygon"]:
            is_within = all(
                is_poly_in_multipoly(coords_1, feature_2[1])
                for coords_1 in feature_1[1]
            )

    return is_within


def boolean_point_on_point(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 point is equal feature_2 point

    :param feature_1: Coordinates of point feature 1
    :param feature_2: Coordinates of point feature 2

    :return: boolean True/False if feature 1 is equal feature 2
    """

    return any(feature_1 == coords_2 for coords_2 in feature_2)


def is_multipoint_on_linestring(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 multipoint feature is in feature_2 polygon
    returns False, if all multipoints are on the boundary

    :param feature_1: Coordinates of multipoint feature
    :param feature_2: Coordinates of polygon feature 2

    :return: boolean True/False if feature 1 is within feature 2
    """

    points_on_line = False

    points_on_line = all(
        boolean_point_on_line(coords_1, feature_2[1]) for coords_1 in feature_1[1]
    )

    if not points_on_line:
        return points_on_line

    points_on_line = any(
        boolean_point_on_line(coords_1, feature_2[1], {"ignoreEndVertices": True})
        for coords_1 in feature_1[1]
    )

    return points_on_line


def is_multipoint_on_polygon(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 multipoint feature is in feature_2 polygon
    returns False, if all multipoints are on the boundary

    :param feature_1: Coordinates of multipoint feature
    :param feature_2: Coordinates of polygon feature 2

    :return: boolean True/False if feature 1 is within feature 2
    """
    points_on_poly = False

    points_on_poly = all(
        boolean_point_in_polygon(coords_1, feature_2[1]) for coords_1 in feature_1[1]
    )

    if not points_on_poly:
        return points_on_poly

    points_on_poly = any(
        boolean_point_in_polygon(coords_1, feature_2[1], {"ignoreBoundary": True})
        for coords_1 in feature_1[1]
    )

    return points_on_poly


def is_line_on_line(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 linestring feature is in feature_2 linestring

    :param feature_1: Coordinates of linestring feature 1
    :param feature_2: Coordinates of linestring feature 2

    :return: boolean True/False if feature 1 is within feature 2
    """

    line_on_line = False

    for coords in feature_1:
        line_on_line = boolean_point_on_line(coords, feature_2)
        if not line_on_line:
            break

    return line_on_line


def is_line_on_multiline(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 linestring feature is in any linestring of feature_2
    multilinestring

    :param feature_1: Coordinates of linestring feature 1
    :param feature_2: Coordinates of multilinestring feature 2

    :return: boolean True/False if feature 1 is within feature 2
    """
    return any(is_line_on_line(feature_1, coords_2) for coords_2 in feature_2)


def is_line_in_poly(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 linestring feature is in feature_2 polygon

    :param feature_1: Coordinates of linestring feature 1
    :param feature_2: Coordinates of polygon feature 2

    :return: boolean True/False if feature 1 is within feature 2
    """
    line_in_poly = False

    line_bbox = bbox(feature_1)
    poly_bbox = bbox(feature_2)

    if not bbox_overlap(poly_bbox, line_bbox):
        return False

    for i in range(len(feature_1) - 1):
        if not boolean_point_in_polygon(feature_1[i], feature_2):
            return False

        if not line_in_poly:
            line_in_poly = boolean_point_in_polygon(
                feature_1[i], feature_2, {"ignoreBoundary": True}
            )

        if not line_in_poly:
            mid = midpoint(point(feature_1[i]), point(feature_1[i + 1]))
            line_in_poly = boolean_point_in_polygon(
                mid, feature_2, {"ignoreBoundary": True}
            )

    return line_in_poly


def is_line_in_multipoly(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 line feature is in any feature_2 multipolygon

    :param feature_1: Coordinates of line feature 1
    :param feature_2: Coordinates of multipolygon feature 2

    :return: boolean True/False if any feature 1 is within any feature 2
    """

    return any(is_line_in_poly(feature_1, coords_2) for coords_2 in feature_2)


def is_poly_in_poly(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 polygon feature is in feature_2 polygon

    :param feature_1: Coordinates of polygon feature 1
    :param feature_2: Coordinates of polygon feature 2

    :return: boolean True/False if feature 1 is within feature 2
    """
    poly_bbox_1 = bbox(feature_1)
    poly_bbox_2 = bbox(feature_2)

    if not bbox_overlap(poly_bbox_2, poly_bbox_1):
        return False

    feature_1 = polygon_to_line(polygon(feature_1))
    line_coords = get_coords_from_features(feature_1)

    for coords in line_coords:
        if not boolean_point_in_polygon(coords, feature_2):
            return False

    return True


def is_poly_in_multipoly(feature_1: Sequence, feature_2: Sequence) -> bool:
    """
    Checks if feature_1 polygon feature is in feature_2 multipolygon

    :param feature_1: Coordinates of polygon feature 1
    :param feature_2: Coordinates of multipolygon feature 2

    :return: boolean True/False if any feature 1 is within feature 2
    """

    return any(is_poly_in_poly(feature_1, coords_2) for coords_2 in feature_2)


def get_features(feature: Any) -> List[Union[str, Sequence]]:
    """
    Takes any feature and returns the geometry type with coordinates.

    :param feature: {GeoJSON} feature any Feature or Geometry

    :return: List of geometry type and coordinate sequence
    """
    feature_coords = get_coords_from_features(feature)
    feature_geometry = get_geometry_type(feature)

    if isinstance(feature_geometry, (list, tuple)):
        feature_geometry = feature_geometry[0]

    return [feature_geometry, feature_coords]


def bbox_overlap(bbox_1: Sequence, bbox_2: Sequence) -> bool:
    """
    Takes two bounding boxes and tests, if bbox_1 is inside bbox2

    :param bbox_1: {List} bounding box of feature 1
    :param bbox_2: {List} bounding box of feature 2

    :return: boolean True/False if bbox 1 is within bbox 2
    """
    if (bbox_1[0] > bbox_2[0]) or (bbox_1[1] > bbox_2[1]):
        return False
    if (bbox_1[2] < bbox_2[2]) or (bbox_1[3] < bbox_2[3]):
        return False

    return True

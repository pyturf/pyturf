from typing import Sequence, Union, Dict

from turf.helpers import Feature
from turf.invariant import get_coords_from_features, get_geometry_from_features
from turf.bbox import bbox as bounding_box
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput

valid_polygons = ["Polygon", "MultiPolygon"]


def boolean_point_in_polygon(
    point: Union[Sequence, Dict, Feature],
    polygon: Union[Dict, Feature],
    options: Dict = None,
):
    """
    Takes a {@link Point} and a Polygon or MultiPolygon and determines if the point
    resides inside the polygon. The polygon can be convex or concave. The function accounts for holes.

    reference:

    http://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
    modified from: https://github.com/substack/point-in-polygon/blob/master/index.js
    which was modified from http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

    :param point: input Point Feature
    :param polygon: input Polygon or MultiPolygon Feature
    :param options: optional parameters
        [options["ignoreBoundary"]] True if polygon boundary should be ignored when determining if
                                    the point is inside the polygon otherwise False.
    :return: True if the Point is inside the Polygon; False otherwise
    """

    if not isinstance(options, dict):
        options = {}

    ignore_boundary = options.get("ignoreBoundary", False)

    point_coords = get_coords_from_features(point, ["Point"])
    polygon_coords = get_coords_from_features(polygon, valid_polygons)

    try:
        polygon_geom_type = get_geometry_from_features(polygon, valid_polygons).get(
            "type"
        )
        if not polygon_geom_type:
            raise AttributeError
    except AttributeError:
        raise InvalidInput(error_code_messages["InvalidGeometry"](valid_polygons))

    bbox = bounding_box(polygon)

    if not in_bbox(point_coords, bbox):
        return False

    if polygon_geom_type == "Polygon":
        polygon_coords = [polygon_coords]

    inside_polygon = False

    for polygon in polygon_coords:
        # check if it is in the outer ring first
        if in_ring(point_coords, polygon[0], ignore_boundary):
            in_hole = False

            for ring in polygon[1:]:
                if in_ring(point_coords, ring, not ignore_boundary):
                    in_hole = True

            if not in_hole:
                inside_polygon = True

        if inside_polygon:
            break

    return inside_polygon


def in_ring(point: Sequence, ring: Sequence, ignore_boundary: bool):
    """
    Checks if point is inside a ring
    :param point: point coordinates [x, y]
    :param ring: ring [[x, y], [x, y], ...]
    :param ignore_boundary: True if polygon boundary should be ignored when determining if
    the point is inside the polygon otherwise False.
    :return: True if point is inside, False otherwise
    """

    is_inside = False

    if ring[0][0] == ring[-1][0] and ring[0][1] == ring[-1][1]:
        ring = ring[:-1]

    i = 0
    j = len(ring) - 1
    while i < len(ring):
        xi = ring[i][0]
        yi = ring[i][1]
        xj = ring[j][0]
        yj = ring[j][1]

        on_boundary = (
            point[1] * (xi - xj) + yi * (xj - point[0]) + yj * (point[0] - xi) == 0
            and ((xi - point[0]) * (xj - point[0]) <= 0)
            and ((yi - point[1]) * (yj - point[1]) <= 0)
        )

        if on_boundary:
            return not ignore_boundary

        intersect = ((yi > point[1]) != (yj > point[1])) and (
            point[0] < (xj - xi) * (point[1] - yi) / (yj - yi) + xi
        )

        if intersect:
            is_inside = not is_inside

        j = i
        i += 1

    return is_inside


def in_bbox(point: Sequence, bbox: Sequence):
    """
    Checks if point is inside bbox

    :param point: point coordinates [lng, lat]
    :param bbox: bbox [west, south, east, north]
    :return: True if point is inside, False otherwise
    """
    return bbox[0] <= point[0] <= bbox[2] and bbox[1] <= point[1] <= bbox[3]

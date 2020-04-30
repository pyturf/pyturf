from typing import Dict, List, Sequence, TypeVar, Union

from turf.bbox import bbox
from turf.explode import explode
from turf.nearest_point import nearest_point

from turf.helpers import (
    all_geometry_types,
    FeatureCollection,
    MultiPolygon,
    Point,
    Polygon,
)
from turf.helpers import feature, feature_collection, geometry, point, polygon
from turf.helpers import Feature, FeatureCollection, Geometry
from turf.invariant import get_coords_from_features
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput

GeoJson = TypeVar("GeoJson", Dict, Feature, FeatureCollection, Geometry)
PointFeature = TypeVar("PointFeature", Dict, Point, Sequence)
PolygonFeature = TypeVar("PolygonFeature", Dict, Polygon, MultiPolygon)


def polygon_tangents(
    start_point: PointFeature, polygon: PolygonFeature
) -> FeatureCollection:
    """ Finds the tangents of a {Polygon or(MultiPolygon} from a {Point}.

    more:
    http://geomalgorithms.com/a15-_tangents.html

    :param point: point [lng, lat] or Point feature to calculate the tangent points from
    :param polygon: polygon to get tangents from

    :return:
        Feature Collection containing the two tangent points
    """
    point_coord = get_coords_from_features(start_point, ("Point",))
    polygon_coords = get_coords_from_features(polygon, ("Polygon", "MultiPolygon"))

    try:
        geometry_type = polygon.get("geometry").get("type")
    except AttributeError:
        try:
            geometry_type = polygon.get("type")
        except AttributeError:
            raise InvalidInput(
                error_code_messages["InvalidGeometry"](["Polygon", "MultiPolygon"])
            )

    box = bbox(polygon)

    near_point_index = 0
    near_point = False

    # If the point lies inside the polygon bbox then it's a bit more complicated
    # points lying inside a polygon can reflex angles on concave polygons
    if (
        (point_coord[0] > box[0])
        and (point_coord[0] < box[2])
        and (point_coord[1] > box[1])
        and (point_coord[1] < box[3])
    ):

        near_point = nearest_point(start_point, explode(polygon))
        near_point_index = near_point["properties"]["featureIndex"]

    if geometry_type == "Polygon":

        tangents = process_polygon(
            polygon_coords, point_coord, near_point, near_point_index
        )

    # bruteforce approach
    # calculate both tangents for each polygon
    # define all tangents as a new polygon and calculate tangetns out of those coordinates
    elif geometry_type == "MultiPolygon":

        multi_tangents = []

        for polygon_coord in polygon_coords:

            tangents = process_polygon(
                polygon_coord, point_coord, near_point, near_point_index
            )
            multi_tangents.extend(tangents)

        tangents = process_polygon(
            [multi_tangents], point_coord, near_point, near_point_index
        )

    r_tangents = tangents[0]
    l_tangents = tangents[1]

    return feature_collection([point(r_tangents), point(l_tangents)])


def process_polygon(
    polygon_coords: Sequence,
    point_coord: Sequence,
    near_point: Union[Point, None],
    near_point_index: int,
) -> Sequence:
    """ Prepares a polygon to calculate the tangents

    :param polygon_coords: point [lng, lat] or Point feature to calculate the tangent points from
    :param point_coord: point [lng, lat]
    :param near_point: nearest point [lng, lat] on polygon towards view point
                         in case the view point lies inside the polygon
    :param near_point_index: index of neareast point on polygon
                        in case the view point lies inside the polygon

    :return:
        List of tangents coordinates [upper and lower]
    """
    r_tangents = polygon_coords[0][near_point_index]
    l_tangents = polygon_coords[0][0]

    if near_point:
        if near_point["geometry"]["coordinates"][1] < point_coord[1]:
            l_tangents = polygon_coords[0][near_point_index]

    tangents = calculate_tangents(
        polygon_coords[0], point_coord, r_tangents, l_tangents,
    )

    return tangents


def calculate_tangents(
    poly_coords: Sequence,
    point_coord: Sequence,
    r_tangents: Sequence,
    l_tangents: Sequence,
) -> Sequence:
    """ Calculate the upper and lower tangents from the polygon by
    comparison with each neighbor coordinate in the polygon

    :param polygon_coords: point [lng, lat] or Point feature to calculate the tangent points from
    :param point_coord: point [lng, lat]
    :param r_tangents: current rightmost tangents point [lng, lat] of the polygon
    :param l_tangents: current leftmost tangents point [lng, lat] of the polygon

    :return:
        List of tangents coordinates [upper and lower]
    """
    edge_next = None
    edge_prev = is_left(poly_coords[0], poly_coords[len(poly_coords) - 1], point_coord,)

    for i in range(1, len(poly_coords) + 1):

        current_poly_coord = poly_coords[i - 1]

        if i == len(poly_coords):
            next_poly_coord = poly_coords[0]
        else:
            next_poly_coord = poly_coords[i]

        edge_next = is_left(current_poly_coord, next_poly_coord, point_coord)

        if (edge_prev <= 0) and (edge_next > 0):

            if not is_below(point_coord, current_poly_coord, r_tangents):
                r_tangents = current_poly_coord

        elif (edge_prev > 0) and (edge_next <= 0):
            if not is_above(point_coord, current_poly_coord, l_tangents):
                l_tangents = current_poly_coord

        edge_prev = edge_next

    return [r_tangents, l_tangents]


def is_above(point1: Sequence, point2: Sequence, point3: Sequence) -> bool:
    """ Checks if point 1 is above point2 and point 3

    :param geojson: geojson or Feature
    :param geojson_types: string of the supposed feature tpye

    :return:
        Feature or FeatureCollection of the incoming geojson
    """
    return is_left(point1, point2, point3) > 0


def is_below(point1: Sequence, point2: Sequence, point3: Sequence) -> bool:
    """ Checks if point 1 is below point2 and point 3

    :param geojson: geojson or Feature
    :param geojson_types: string of the supposed feature tpye

    :return:
        Feature or FeatureCollection of the incoming geojson
    """
    return is_left(point1, point2, point3) < 0


def is_left(point1: Sequence, point2: Sequence, point3: Sequence) -> float:
    """ Calculates if point 1 is left of point2 and point 3

    :param geojson: geojson or Feature
    :param geojson_types: string of the supposed feature tpye

    :return:
        Feature or FeatureCollection of the incoming geojson
    """
    return (point2[0] - point1[0]) * (point3[1] - point1[1]) - (
        point3[0] - point1[0]
    ) * (point2[1] - point1[1])

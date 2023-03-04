from typing import List, TypeVar, Union

from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf.center import center
from turf.explode import explode
from turf.invariant import get_coords_from_features, get_geometry_type

from turf.nearest_point import nearest_point
from turf.helpers import Feature, FeatureCollection, Point
from turf.helpers import feature, feature_collection, point, polygon, multi_polygon
from turf.helpers._features import all_geometry_types
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput

from turf.boolean_point_on_line import boolean_point_on_line

GeoJSON = TypeVar("GeoJSON", Feature, FeatureCollection)


def point_on_feature(features: GeoJSON) -> Point:
    """
    Takes a Feature or FeatureCollection and returns a {Point} guaranteed to be on the surface of the feature.

    Given a {Polygon}, the point will be in the area of the polygon
    Given a {LineString}, the point will be along the string
    Given a {Point}, the point will the same as the input

    :param features: any GeoJSON feature or feature collection
    :return: Point GeoJSON Feature on the surface of `input`
    """
    feature_collection = normalize_to_feature_collection(features)

    center_point = center(feature_collection)
    center_coords = center_point.get("geometry").get("coordinates")

    # check to see if centroid is on surface
    center_on_surface = False

    geometry_type = get_geometry_type(feature_collection)
    geometry_coords = get_coords_from_features(feature_collection)

    if isinstance(geometry_type, str):
        geometry_type = [geometry_type]

    for geo_type, geo_coords in zip(geometry_type, geometry_coords):
        if geo_type in ["Point", "MultiPoint"]:
            if geo_type == "Point":
                geo_coords = [geo_coords]

            for point_coords in geo_coords:
                if (center_coords[0] == point_coords[0]) and (
                    center_coords[1] == point_coords[1]
                ):
                    center_on_surface = True
                    break

        elif geo_type in ["LineString", "MultiLineString"]:
            if geo_type == "LineString":
                geo_coords = [geo_coords]

            for line_coords in geo_coords:
                if boolean_point_on_line(center_coords, line_coords):
                    center_on_surface = True
                    break

        elif geo_type in ["Polygon", "MultiPolygon"]:
            if geo_type == "Polygon":
                geo_coords = polygon(geo_coords)
            else:
                geo_coords = multi_polygon(geo_coords)
            if boolean_point_in_polygon(center_point, geo_coords):
                center_on_surface = True
                break

    if center_on_surface:
        point_on_surface = center_point

    else:
        point_on_surface = nearest_point(center_point, feature_collection)

    return point_on_surface


def normalize_to_feature_collection(geojson: GeoJSON) -> FeatureCollection:
    """
    Normalizes any GeoJSON to a FeatureCollection

    :param geojson: any GeoJSON
    :return: FeatureCollection
    """
    geojson_type = geojson.get("type")

    if geojson_type == "FeatureCollection":
        pass

    elif geojson_type == "Feature":
        geojson = feature_collection([geojson])

    else:
        geojson = feature_collection([feature(geojson)])

    return geojson

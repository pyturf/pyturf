from typing import List, TypeVar, Union

import numpy as np

from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf.center import center
from turf.explode import explode
from turf.nearest_point import nearest_point
from turf.helpers import Feature, FeatureCollection, Point
from turf.helpers import feature, feature_collection, point
from turf.helpers._features import all_geometry_types
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


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

    for feature in feature_collection["features"]:

        geometry_type = feature.get("geometry").get("type")
        geometry_coords = feature.get("geometry").get("coordinates")

        if geometry_type in ["Point", "MultiPoint"]:

            if geometry_type == "Point":
                geometry_coords = [geometry_coords]

            for point_coords in geometry_coords:

                if (center_coords[0] == point_coords[0]) and (
                    center_coords[1] == point_coords[1]
                ):

                    center_on_surface = True
                    break

        elif geometry_type in ["LineString", "MultiLineString"]:

            if geometry_type == "LineString":
                geometry_coords = [geometry_coords]

            for line in geometry_coords:

                for seg_index in range(1, len(line)):

                    if point_on_segment(
                        center_coords, line[seg_index - 1], line[seg_index]
                    ):

                        center_on_surface = True
                        break

        elif geometry_type in ["Polygon", "MultiPolygon"]:

            if boolean_point_in_polygon(center_point, feature):
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


def point_on_segment(point: List, segment_start: List, segment_end: List) -> bool:
    """
    Checks if a given point is on a line or not

    :param point: Coordinates of a point
    :param segment_start: Coordinates of the start line
    :param segment_end: Coordinates of the line end
    :return: bool
    """

    len_segment = np.sqrt(
        np.power(segment_end[0] - segment_start[0], 2)
        + np.power(segment_end[1] - segment_start[1], 2)
    )
    len_point_seg_1 = np.sqrt(
        np.power(point[0] - segment_start[0], 2)
        + np.power(point[1] - segment_start[1], 2)
    )
    len_point_seg_2 = np.sqrt(
        np.power(segment_end[0] - point[0], 2) + np.power(segment_end[1] - point[1], 2)
    )

    return len_segment == len_point_seg_1 + len_point_seg_2

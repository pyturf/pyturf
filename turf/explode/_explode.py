from typing import Dict, List, Sequence, TypeVar

from turf.invariant import get_coords_from_features, get_coords_from_geometry

from turf.helpers import feature_collection, point
from turf.helpers import Feature, FeatureCollection, Geometry

from turf.utils.helpers import get_input_dimensions
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.helpers._features import all_geometry_types

GeoJson = TypeVar("GeoJson", Dict, Feature, FeatureCollection, Geometry)


def explode(features: GeoJson) -> FeatureCollection:
    """
    Takes a feature or set of features and returns all positions as {Point|points}.

    :param features: any GeoJSON feature or feature collection
    :return: {FeatureCollection} points representing the exploded input features
    """
    points = []

    try:
        geojson_type = features.get("type")
    except AttributeError:
        raise InvalidInput(error_code_messages["InvalidGeometry"](all_geometry_types))

    if geojson_type in ["FeatureCollection", "GeometryCollection"]:

        key = "features" if geojson_type == "FeatureCollection" else "geometries"

        for feature in features[key]:

            properties = feature.get("properties", {})
            coords = get_coords_from_features(feature)
            points.extend(reduce_coordinates_to_points(coords, properties))

    else:

        properties = features.get("properties", {})
        coords = get_coords_from_geometry(features)
        points.extend(reduce_coordinates_to_points(coords, properties))

    return feature_collection(points)


def reduce_coordinates_to_points(
    coords: Sequence, properties: Dict
) -> Sequence[Feature]:
    """
    Transforms dimensionality of the incoming coordinates into Point Features

    :param coords: any sequence of coordinates
    :param properties: properties of the coordinates sequence
    :return: {Feature} points of transformed coordinates
    """

    dim = get_input_dimensions(coords)

    if dim == 1:
        coords = [coords]

    while dim > 2:
        coords = [c for coord in coords for c in coord]
        dim = get_input_dimensions(coords)

    points = [point(coord, properties) for coord in coords]

    return points

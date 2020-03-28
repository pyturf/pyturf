from turf.helpers import (
    Feature,
    Point,
    LineString,
    MultiPoint,
    MultiLineString,
    Polygon,
    MultiPolygon,
    FeatureCollection,
    get_input_dimensions,
)
from turf.utils.exceptions import InvalidInput
from turf.utils.error_codes import error_code_messages
from turf.utils.helpers import dimensions

allowed_types_points = ["Point", "MultiPoint"]
allowed_types_default = ["Point", "Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"]


def get_coords_from_geometry(geometry, allowed_types=None, raise_exception=True):
    if not allowed_types:
        allowed_types = allowed_types_default

    if isinstance(geometry, list):
        allowed_input_dimensions = [dimensions[allowed_type] for allowed_type in allowed_types]

        if get_input_dimensions(geometry) in allowed_input_dimensions:
            return geometry
        else:
            if raise_exception:
                raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_types))
            return []

    if isinstance(geometry, (Feature, dict)):
        if geometry.get("type") == "Feature":
            return get_coords_from_geometry(geometry.get("geometry", {}), allowed_types)

    allowed_class_types = [
        *[eval(allowed_type) for allowed_type in allowed_types],
        dict,
    ]

    if any(
        isinstance(geometry, allowed_type_class)
        for allowed_type_class in allowed_class_types
    ):
        return geometry.get("coordinates", [])

    if raise_exception:
        raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_types))
    else:
        return []


def get_geometry_from_features(features, allowed_types=None):

    if not allowed_types:
        allowed_types = ["Point", "Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"]

    if isinstance(features, list):
        allowed_input_dimensions = [sub for allowed_type in allowed_types for sub in (dimensions[allowed_type], 1)]

        if get_input_dimensions(features) in allowed_input_dimensions:
            return [features]
        else:
            raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_types))

    if isinstance(features, (FeatureCollection, dict)):
        if features.get("type") == "FeatureCollection":
            return list(
                map(
                    lambda feature: feature.get("geometry", {}),
                    features.get("features", []),
                )
            )

    if isinstance(features, (Feature, dict)):
        if features.get("type") == "Feature":
            return [features.get("geometry", {})]

    raise InvalidInput(error_code_messages["InvalidFeature"])


def get_coords_from_features(features, allowed_types=None):

    if not allowed_types:
        allowed_types = allowed_types_default

    if isinstance(features, (FeatureCollection, dict)):
        if features.get("type") == "FeatureCollection":
            return list(
                map(
                    lambda feature: get_coords_from_geometry(
                        feature.get("geometry", {}),
                        allowed_types
                    ),
                    features.get("features", []),
                )
            )

    if isinstance(features, list) and all(
        isinstance(sub_list, list) for sub_list in features
    ):
        return features

    return get_coords_from_geometry(features, allowed_types)


def get_coord(coord):
    if get_input_dimensions(coord) == 1 and len(coord) == 2:
        return coord

    elif (
        isinstance(coord, Feature)
        and getattr(coord, "geometry", None)
        and getattr(coord.geometry, "type", None) in allowed_types_points
    ):
        return coord.geometry.coordinates

    elif isinstance(coord, (Point, MultiPoint)):
        return coord.coordinates

    elif isinstance(coord, dict) and coord.get("type", None) == "Feature":
        if (
            "geometry" in coord
            and coord["geometry"].get("type", None) in allowed_types_points
            and "coordinates" in coord["geometry"]
        ):
            return coord["geometry"]["coordinates"]

    elif isinstance(coord, dict) and coord.get("type", None) in allowed_types_points:
        if "coordinates" in coord:
            return coord["coordinates"]

    raise InvalidInput(error_code_messages["InvalidPoint"])

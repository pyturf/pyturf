from typing import Any, Sequence, Callable, Set, List, Union

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
allowed_types_default = [
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]


def _process_list_input(
    allowed_types: Sequence,
    input_value: Sequence,
    callback: Callable,
    raise_exception: bool = True,
) -> List:
    """
    Retrieves the coords from lists, or raises an exception if invalid.

    :param allowed_types: allowed Feature types
    :param input_value: list input
    :param callback: method to call recursively
    :param raise_exception: if an exception should be raised or if it should be silent
    :return: list with extracted coords
    """

    dim = get_input_dimensions(input_value)

    allowed_dimensions = {dimensions.get(type_, None) for type_ in allowed_types}

    allowed_class_types = (
        *[eval(allowed_type) for allowed_type in allowed_types],
        dict,
    )

    if dim == 1 and all(isinstance(el, allowed_class_types) for el in input_value):
        return list(map(lambda geom: callback(geom, allowed_types), input_value))

    return _check_input_in_allowed_dimensions(
        input_value, dim, allowed_types, allowed_dimensions, raise_exception
    )


def _check_input_in_allowed_dimensions(
    input_value: Sequence,
    dim: int,
    allowed_types: Sequence,
    allowed_dimensions: Set,
    raise_exception: bool = True,
) -> Union[List, Sequence]:
    """
    :param input_value: list input
    :param dim: number of dimensions of input
    :param allowed_types: allowed Feature types
    :param allowed_dimensions: allowed dimensions for specified allowed types
    :param raise_exception: if an exception should be raised or if it should be silent
    :return: list with extracted coords
    """
    if dim in allowed_dimensions:
        if dim == 1 and len(input_value) < 2:
            raise InvalidInput(error_code_messages["InvalidPointInput"])

        return input_value
    else:
        if raise_exception:
            raise InvalidInput(
                error_code_messages["InvalidGeometry"](
                    [type_ for type_ in allowed_types if type_ in allowed_types_default]
                )
            )
        return []


def get_coords_from_geometry(
    geometry: Any, allowed_types: Sequence = None, raise_exception: bool = True
) -> List:
    """
    Retrieves coords from a given Geometry. Geometry must be a GeoJSON,
    a Geometry object or a list of coordinates, otherwise it raises an exception.

    :param geometry: Any input value(s)
    :param allowed_types: allowed Feature types
    :param raise_exception: if an exception should be raised or if it should be silent
    :return: list with extracted coords
    """

    if not allowed_types:
        allowed_types = allowed_types_default

    if isinstance(geometry, list):
        return _process_list_input(
            allowed_types, geometry, get_coords_from_geometry, raise_exception
        )

    if isinstance(geometry, (Feature, dict)):
        if geometry.get("type") == "Feature":
            return get_coords_from_geometry(geometry.get("geometry", {}), allowed_types)

    allowed_class_types = [
        *[eval(allowed_type) for allowed_type in allowed_types],
        dict,
    ]

    if any(
        isinstance(geometry, allowed_type_class)
        and geometry.get("type", "") in allowed_types
        for allowed_type_class in allowed_class_types
    ):
        return geometry.get("coordinates", [])

    if raise_exception:
        raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_types))
    else:
        return []


def get_geometry_from_features(features: Any, allowed_types: Sequence = None) -> List:
    """
    Retrieves Geometries from Features. Features must be a GeoJSON,
    a Feature object or a list of coordinates, otherwise it raises an exception.

    :param features: Any input value(s)
    :param allowed_types: allowed Feature types
    :return: list with extracted coords
    """

    if not allowed_types:
        allowed_types = allowed_types_default

    if isinstance(features, list):
        return _process_list_input(
            [*allowed_types, "Feature"], features, get_geometry_from_features
        )

    if isinstance(features, (FeatureCollection, dict)):
        if features.get("type") == "FeatureCollection":
            return list(
                map(
                    lambda feature: feature.get("geometry", {}),
                    features.get("features", []),
                )
            )

    if isinstance(features, (Feature, dict)):
        if features.get("type", "") == "Feature":
            if features.get("geometry", {}).get("type", "") in allowed_types:
                return features.get("geometry", {})

    if isinstance(
        features, (*[eval(allowed_type) for allowed_type in allowed_types], dict)
    ):
        if features.get("type", "") in allowed_types:
            return features

    raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_types))


def get_coords_from_features(features: Any, allowed_types: Sequence = None) -> List:
    """
    Retrieves coords from Features. Features must be a GeoJSON,
    a Feature object or a list of coordinates, otherwise it raises an exception.

    :param features: Any input value(s)
    :param allowed_types: allowed Feature types
    :return: list with extracted coords
    """

    if not allowed_types:
        allowed_types = allowed_types_default

    if isinstance(features, (FeatureCollection, dict)):
        if features.get("type") == "FeatureCollection":
            return list(
                map(
                    lambda feature: get_coords_from_geometry(
                        feature.get("geometry", {}), allowed_types
                    ),
                    features.get("features", []),
                )
            )

    return get_coords_from_geometry(features, allowed_types)

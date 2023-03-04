from typing import Any, Sequence, Callable, Set, List, Tuple, Union

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
allowed_features_default = (
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
)


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

    if isinstance(geometry, (list, tuple)):
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

    if isinstance(features, (list, tuple)):
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


def get_geometry_type(
    features: Any, allowed_types: Sequence = None
) -> Union[str, Tuple[str]]:
    """
    Gets the Geometry type from Features. Features must be a GeoJSON,
    a Feature object, FeatureCollection a Dictionary, List or a Tuple, otherwise it raises an exception.

    :param features: Any input value(s)
    :param allowed_types: allowed Feature types
    :return: str if one extracted geometry_type else tuple
    """
    if not allowed_types:
        allowed_features = [allowed_features_default, allowed_types_default]

    else:
        allowed_features = [
            tuple(
                [
                    feature
                    for feature in allowed_features_default
                    if feature.__name__ in allowed_types
                ]
            ),
            allowed_types,
        ]

    features = get_geometry_from_features(features, allowed_features[1])

    if isinstance(features, (dict, *allowed_features[0])):
        geometry_type = _get_geometry_type_from_feature(features, allowed_features)

    elif isinstance(features, (list, tuple)):
        geometry_type = _get_geometry_type_from_list(features, allowed_features)

    else:
        raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_features[1]))

    if len(geometry_type) == 1:
        geometry_type = geometry_type[0]

    return geometry_type


def _get_geometry_type_from_feature(
    features: Any, allowed_features: List[Union[Tuple, Sequence]]
) -> str:
    """
    Gets the Geometry type from a Features. Features must be a GeoJSON,
    a Feature object, FeatureCollection or a Dictionary, otherwise it raises an exception.

    :param features: Any input value(s) except a list
    :return: tuple with extracted geometry types
    """
    geometry_type = features.get("type", None)

    if geometry_type not in allowed_features[1]:
        raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_features[1]))

    return geometry_type


def _get_geometry_type_from_list(
    features: List, allowed_features: List[Union[Tuple, Sequence]]
) -> Tuple[str]:
    """
    Gets the Geometry type from a List, otherwise it raises an exception.

    :param features: input feature as a list
    :return: tuple with extracted geometry types
    """
    geometry_type = tuple()

    n_dim = get_input_dimensions(features)

    if n_dim == 1 and all(
        isinstance(el, (dict, *allowed_features[0])) for el in features
    ):
        return tuple(
            map(
                lambda geom: _get_geometry_type_from_feature(geom, allowed_features),
                features,
            )
        )

    elif all(isinstance(el, (list, tuple, int, float)) for el in features):
        feature_type = [
            k for k, v in dimensions.items() if v == n_dim and k in allowed_features[1]
        ]
        if len(feature_type) == 1:
            geometry_type += (feature_type[0],)

        else:
            raise InvalidInput(
                error_code_messages["InvalidGeometry"](allowed_features[1])
            )

    else:
        raise InvalidInput(error_code_messages["InvalidGeometry"](allowed_features[1]))

    return geometry_type


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

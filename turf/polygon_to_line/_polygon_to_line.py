from typing import Dict, Sequence, TypeVar

from turf.helpers import (
    Feature,
    FeatureCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Polygon,
)

from turf.helpers import feature_collection, line_string, multi_line_string
from turf.invariant import get_coords_from_features
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


PolygonFeature = TypeVar(Dict, "PolygonFeature", Polygon, MultiPolygon)
LineFeature = TypeVar(
    "LineFeature", Dict, Feature, FeatureCollection, LineString, MultiLineString
)


def polygon_to_line(polygon: PolygonFeature, options: Dict = {}) -> LineFeature:
    """ Converts a {Polygon} to a {LineString} or a {MultiPolygon} to a {FeatureCollection}
    or {MultiLineString}.

    :param polygon: Feature to convert
    :param options: Optional parameters

    :return:
        {Feature Collection|LineString|MultiLineString} of converted (Multi)Polygon to (Multi)LineString
    """
    if not options:
        properties = polygon.get("properties", {})
    else:
        properties = options.get("properties", {})

    try:
        geometry_type = polygon.get("geometry").get("type")
    except AttributeError:
        try:
            geometry_type = polygon["type"]
        except KeyError:
            raise InvalidInput(
                error_code_messages["InvalidGeometry"](["Polygon", "MultiPolygon"])
            )

    polygon_coords = get_coords_from_features(polygon, ("Polygon", "MultiPolygon"))

    if geometry_type == "MultiPolygon":

        line_coords = []

        for polygon_coord in polygon_coords:

            line_coords.append(coords_to_line(polygon_coord, properties))

        line_feature = feature_collection(line_coords)

    else:

        line_feature = coords_to_line(polygon_coords, properties)

    return line_feature


def coords_to_line(coords: Sequence, properties: Dict) -> LineFeature:
    """ Converts coordinates to a {LineString}} or {MultiLineString}.

    :param polygon: Feature to convert
    :param properties: Optional parameters

    :return:
        {feature} of a (Multi)LineString
    """

    if len(coords) > 1:

        feature = multi_line_string(coords, properties)

    else:

        feature = line_string(coords[0], properties)

    return feature

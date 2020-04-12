from abc import ABC
from typing import List, Dict, Any, Iterable, Union, Sequence

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.helpers import get_input_dimensions


all_geometry_types = [
    "Point",
    "LineString",
    "Polygon",
    "MultiPoint",
    "MultiLineString",
    "MultiPolygon",
]


class Geometry(ABC):
    """
    Base class for Point, LineString and Polygon sub-classes.
    """

    def __init__(self, coordinates: Iterable, geometry_type) -> None:

        self._check_input(coordinates)
        self.coordinates = coordinates
        self.type = geometry_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.coordinates})"

    def __eq__(self, other: Any) -> bool:
        try:
            equality = self.type == other.type
            equality &= self.coordinates == other.coordinates
        except AttributeError:
            return False

        return equality

    def get(self, attribute: str, default=None) -> Any:
        try:
            return getattr(self, attribute)
        except AttributeError:
            return default

    @classmethod
    def from_geojson(cls, geojson: Dict) -> Any:
        try:
            coords = geojson["coordinates"]
        except KeyError:
            raise InvalidInput(error_code_messages["InvalidCoordinates"])

        return geometry(cls.__name__, coords, as_geojson=False)

    def to_geojson(self) -> Dict:
        """
        Translates the object into a GeoJSON feature.

        :return: a GeoJSON feature as a dict
        """

        return {"type": self.type, "coordinates": self.coordinates}


class Point(Geometry):
    """
    Class for creating Point objects with certain coordinates.
    Equivalent to a GeoJSON Point.
    """

    def __init__(self, coordinates: Sequence) -> None:
        Geometry.__init__(self, coordinates, "Point")

    @staticmethod
    def _check_input(coordinates: Sequence) -> None:
        """
        Checks input given to Point class, and raises an error if input is invalid.

        :param coordinates: input coordinates
        """

        if (
            get_input_dimensions(coordinates) == 1
            and len(coordinates) == 2
            and all(isinstance(x, (int, float)) for x in coordinates)
        ):
            return

        raise InvalidInput(error_code_messages["InvalidPointInput"])


class MultiPoint(Point):
    def __init__(self, coordinates: Sequence) -> None:
        Point.__init__(self, coordinates)
        self.type = "MultiPoint"

    def _check_input(self, coordinates: Sequence) -> None:
        """
        Checks input given to MultiPoint class, and raises an error if input is invalid.

        :param coordinates: input coordinates
        """

        if get_input_dimensions(coordinates) != 2:
            raise InvalidInput(error_code_messages["InvalidMultiInput"] + "of Points")

        for coord in coordinates:
            super(MultiPoint, self)._check_input(coord)


class LineString(Geometry):
    """
    Class for creating LineString objects with certain coordinates.
    Equivalent to a GeoJSON LineString.
    """

    def __init__(self, coordinates: Sequence) -> None:
        Geometry.__init__(self, coordinates, geometry_type="LineString")

    def _check_input(self, coordinates: Sequence) -> None:
        """
        Checks input given to LineString class, and raises an error if input is invalid.

        :param coordinates: input coordinates
        """

        if get_input_dimensions(coordinates) != 2:
            raise InvalidInput(error_code_messages["InvalidLineStringInput"])

        if len(coordinates) >= 2 and all(
            all(isinstance(x, (int, float)) for x in y) for y in coordinates
        ):
            return

        raise InvalidInput(error_code_messages["InvalidLinePoints"])


class MultiLineString(LineString):
    def __init__(self, coordinates: Sequence) -> None:
        LineString.__init__(self, coordinates)
        self.type = "MultiLineString"

    def _check_input(self, coordinates: Sequence) -> None:
        """
        Checks input given to MultiLineString class, and raises an error if input is invalid.

        :param coordinates: input coordinates
        """

        if get_input_dimensions(coordinates) != 3:
            raise InvalidInput(
                error_code_messages["InvalidMultiInput"] + "of LineStrings"
            )

        for coord in coordinates:
            super(MultiLineString, self)._check_input(coord)


class Polygon(Geometry):
    """
    Class for creating Polygon objects with certain coordinates.
    Equivalent to a GeoJSON Polygon.
    """

    def __init__(self, coordinates: Sequence) -> None:
        Geometry.__init__(self, coordinates, geometry_type="Polygon")

    def _check_input(self, coordinates: Sequence) -> None:
        """
        Checks input given to Polygon class, and raises an error if input is invalid.

        :param coordinates: input coordinates
        """

        if get_input_dimensions(coordinates) != 3:
            raise InvalidInput(error_code_messages["InvalidPolygonInput"])

        for ring in coordinates:
            if not isinstance(ring, list):
                raise InvalidInput(error_code_messages["InvalidLinearRing"])

            if len(ring) < 4:
                raise InvalidInput(error_code_messages["InvalidLinearRing"])

            if ring[-1] != ring[0]:
                raise InvalidInput(error_code_messages["InvalidFirstLastPoints"])


class MultiPolygon(Polygon):
    def __init__(self, coordinates: Sequence) -> None:
        Polygon.__init__(self, coordinates)
        self.type = "MultiPolygon"

    def _check_input(self, coordinates: Sequence) -> None:
        """
        Checks input given to MultiPolygon class, and raises an error if input is invalid.

        :param coordinates: input coordinates
        """

        if get_input_dimensions(coordinates) != 4:
            raise InvalidInput(error_code_messages["InvalidMultiInput"] + "of Polygons")

        for coord in coordinates:
            super(MultiPolygon, self)._check_input(coord)


class FeatureType:
    """
    Parent class for Feature and FeatureCollection.
    """

    def __init__(self, feature_type: str) -> None:
        self.type = feature_type

    def get(self, attribute: str, default=None) -> Any:
        try:
            return getattr(self, attribute)
        except AttributeError:
            return default


class Feature(FeatureType):
    """
    Class that encapsulates a certain geometry, along with its properties.
    Equivalent to a GeoJSON feature.
    """

    def __init__(
        self,
        geom: Union[
            Dict, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon,
        ],
        properties: Union[Dict, None] = None,
    ) -> None:

        geom = self._check_input(geom)

        FeatureType.__init__(self, feature_type="Feature")

        self.geometry = geom
        self.properties = properties or {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.geometry})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Feature):
            return False

        equality = self.geometry.type == other.geometry.type
        equality &= self.geometry.coordinates == other.geometry.coordinates

        return equality

    @staticmethod
    def _check_input(
        geom: Union[
            Dict, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon,
        ]
    ) -> Union[
        Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon,
    ]:
        """
        Checks input given to Feature class, and converts to object if input is in dict form.

        :param geom: input geometry
        :return: geometry object
        """

        if not any(isinstance(geom, eval(cls)) for cls in all_geometry_types):
            if isinstance(geom, dict):
                feat_type = geom.get("type", "nonexistent")
                try:
                    return eval(feat_type).from_geojson(geom)
                except (NameError, AttributeError):
                    raise InvalidInput(
                        error_code_messages["InvalidGeometry"](all_geometry_types)
                    )
            else:
                raise InvalidInput(
                    error_code_messages["InvalidGeometry"](all_geometry_types)
                )

        return geom

    def to_geojson(self) -> Dict:
        """
        Translates the object into a GeoJSON feature.

        :return: a GeoJSON feature as a dict
        """

        geojson = {
            "type": "Feature",
            "properties": self.properties,
            "geometry": self.geometry.to_geojson(),
        }

        if self.get("bbox"):
            geojson["bbox"] = self.get("bbox")

        return geojson


class FeatureCollection(FeatureType):
    """
    Class that encapsulates a group of features in a FeatureCollection.
    Equivalent to a GeoJSON FeatureCollection.
    """

    def __init__(self, features: Sequence = None) -> None:

        features = self._check_input(features)

        FeatureType.__init__(self, feature_type="FeatureCollection")

        self.features = features or []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({[feat.get('geometry').get('type') for feat in self.features]})"

    @staticmethod
    def _check_input(features: Sequence,) -> List[Union[Dict, Feature]]:
        """
        Checks input given to FeatureCollection class, and converts to list of
        Feature objects if input is in dict form.

        :param features: input features
        :return: a list of the feature objects
        """

        if not isinstance(features, list):
            raise InvalidInput(error_code_messages["InvalidFeatureCollection"])

        eval_feats = []
        for feat in features:
            if not isinstance(feat, Feature):

                if isinstance(feat, dict):
                    feat_type = feat.get("geometry", {}).get("type", "nonexistent")
                    try:
                        geom = eval(feat_type).from_geojson(feat.get("geometry", {}))
                        properties = feat.get("properties", None)
                        feat_from_geojson = feature(
                            geom, properties=properties, as_geojson=False
                        )

                        eval_feats.append(feat_from_geojson)
                    except NameError:
                        raise InvalidInput(
                            error_code_messages["InvalidGeometry"](all_geometry_types)
                        )
                else:
                    raise InvalidInput(
                        error_code_messages["InvalidGeometry"](all_geometry_types)
                    )

            else:
                eval_feats.append(feat)

        return eval_feats

    def to_geojson(self) -> Dict:
        """
        Translates the object into a GeoJSON feature.

        :return: a GeoJSON feature as a dict
        """

        geojson = {"type": "FeatureCollection", "features": []}

        for f in self.features:
            geojson["features"].append(f.to_geojson())

        return geojson


def feature(
    geom: (Dict, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon),
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[Feature, Dict]:
    """
    Wraps a GeoJSON Geometry in a GeoJSON Feature.

    :param geom: input geometry
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a GeoJSON feature
    """

    if not options:
        options = {}

    if not properties:
        properties = {}

    feat = Feature(geom, properties)

    if "id" in options:
        feat.id = options["id"]

    if "bbox" in options:
        feat.bbox = options["bbox"]

    return feat.to_geojson() if as_geojson else feat


def feature_collection(
    features: Sequence, options: Dict = None, as_geojson: bool = True
) -> Union[FeatureCollection, Dict]:
    """
    Takes one or more Feature and creates a FeatureCollection.

    :param features: input features
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a FeatureCollection of Features
    """

    if not options:
        options = {}

    feat_collection = FeatureCollection(features)

    if "id" in options:
        feat_collection.id = options["id"]

    if "bbox" in options:
        feat_collection.bbox = options["bbox"]

    return feat_collection.to_geojson() if as_geojson else feat_collection


def geometry(
    geom_type: str, coordinates: Sequence, as_geojson: bool = True
) -> Union[
    Dict, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon,
]:
    """
    Creates a GeoJSON {@link Geometry} from a Geometry string type & coordinates.
    For GeometryCollection type use `helpers.geometryCollection`

    :param geom_type: one of "Point" | "LineString" | "Polygon" | "MultiPoint" | "MultiLineString" | "MultiPolygon"
    :param coordinates: array of coordinates [lng, lat]
    :param as_geojson: whether the return value should be a geojson
    :return: a GeoJSON geometry
    """

    if geom_type == "Point":
        geom = Point(coordinates)
    elif geom_type == "LineString":
        geom = LineString(coordinates)
    elif geom_type == "Polygon":
        geom = Polygon(coordinates)
    elif geom_type == "MultiPoint":
        geom = MultiPoint(coordinates)
    elif geom_type == "MultiLineString":
        geom = MultiLineString(coordinates)
    elif geom_type == "MultiPolygon":
        geom = MultiPolygon(coordinates)
    else:
        raise InvalidInput(error_code_messages["InvalidGeometry"](all_geometry_types))

    return geom.to_geojson() if as_geojson else geom


def point(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[Point, Dict]:
    """
    Creates a Point Feature from a Position.

    :param coordinates: coordinates longitude, latitude position in degrees - Position
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a Point Feature
    """

    geom = Point(coordinates)

    return feature(geom, properties, options, as_geojson=as_geojson)


def points(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[FeatureCollection, Dict]:
    """
    Creates a Point FeatureCollection from an Array of Point coordinates.

    :param coordinates: a list of Points - Position[]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: Point FeatureCollection
    """

    if not isinstance(coordinates, list):
        raise Exception("Coordinates must be a list")

    return feature_collection(
        list(map(lambda coord: point(coord, properties), coordinates)),
        options,
        as_geojson=as_geojson,
    )


def multi_point(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[MultiPoint, Dict]:
    """
    Creates a MultiPoint Feature based on a coordinate array.
    Properties can be added optionally.

    :param coordinates: a list of Points - Position[]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a MultiPoint feature
    """

    geom = MultiPoint(coordinates)

    return feature(geom, properties, options, as_geojson=as_geojson)


def line_string(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[LineString, Dict]:
    """
    Creates a LineString Feature from an Array of Positions.

    :param coordinates: a list of Positions - Position[]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a LineString feature
    """

    if not options:
        options = {}

    if not properties:
        properties = {}

    geom = LineString(coordinates)

    return feature(geom, properties, options, as_geojson=as_geojson)


def line_strings(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[FeatureCollection, Dict]:
    """
    Creates a LineString FeatureCollection from an Array of LineString coordinates.

    :param coordinates: a list of a list of Positions - Position[][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: LineString FeatureCollection
    """

    if not isinstance(coordinates, list):
        raise Exception("Coordinates_list must be a list")

    return feature_collection(
        list(map(lambda coord: line_string(coord, properties), coordinates)),
        options,
        as_geojson=as_geojson,
    )


def multi_line_string(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[MultiLineString, Dict]:
    """
    Creates a MultiLineString Feature based on a coordinate array.
    Properties can be added optionally.

    :param coordinates: a list of a list of Positions - Position[][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a MultiLineString feature
    """

    geom = MultiLineString(coordinates)

    return feature(geom, properties, options, as_geojson=as_geojson)


def polygon(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[Polygon, Dict]:
    """
    Creates a Polygon Feature from an Array of LinearRings.

    :param coordinates: a list of a list of Positions - Position[][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a Polygon Feature
    """

    if not options:
        options = {}

    if not properties:
        properties = {}

    geom = Polygon(coordinates)

    return feature(geom, properties, options, as_geojson=as_geojson)


def polygons(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[FeatureCollection, Dict]:
    """
    Creates a Polygon FeatureCollection from an Array of Polygon coordinates.

    :param coordinates: an array of polygons - Position[][][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: Polygon FeatureCollection
    """

    if not isinstance(coordinates, list):
        raise Exception("Coordinates_list must be a list")

    return feature_collection(
        list(map(lambda coords: polygon(coords, properties), coordinates)),
        options,
        as_geojson=as_geojson,
    )


def multi_polygon(
    coordinates: Sequence,
    properties: Dict = None,
    options: Dict = None,
    as_geojson: bool = True,
) -> Union[MultiPolygon, Dict]:
    """
    Creates a MultiPolygon Feature based on a coordinate array.
    Properties can be added optionally.

    :param coordinates: an array of polygons - Position[][][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :param as_geojson: whether the return value should be a geojson
    :return: a MultiPolygon feature
    """

    geom = MultiPolygon(coordinates)

    return feature(geom, properties, options, as_geojson=as_geojson)

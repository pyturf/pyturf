import pytest

from turf.helpers._features import (
    point,
    line_string,
    polygon,
    points,
    line_strings,
    polygons,
    multi_point,
    multi_line_string,
    multi_polygon,
    feature,
    Point,
    feature_collection,
    geometry,
)
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


class TestPoint:
    def test_coordinates_props(self):

        p = point([5, 10], {"name": "test point"}, as_geojson=False)

        assert p.geometry.coordinates[0] == 5
        assert p.geometry.coordinates[1] == 10
        assert p.geometry.type == "Point"
        assert p.properties["name"] == "test point"

    def test_no_props(self):

        p = point([0, 0], as_geojson=False)

        assert p.get("properties") == {}

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                [1], error_code_messages["InvalidPointInput"], id="InvalidPointInput",
            ),
            pytest.param(
                [1, "xyz"],
                error_code_messages["InvalidPointInput"],
                id="InvalidPointInput",
            ),
        ],
    )
    def test_exceptions(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            point(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

    def test_points(self):

        pts = points(
            [[-75, 39], [-80, 45], [-78, 50]],
            {"foo": "bar"},
            {"id": "hello"},
            as_geojson=False,
        )

        assert len(pts.features) == 3
        assert pts.id == "hello"
        assert pts.features[0].properties["foo"] == "bar"

    def test_multi_point(self):

        mp = multi_point([[0, 0], [10, 10]], {"test": 23}, as_geojson=False)

        assert mp.type == "Feature"
        assert mp.properties == {"test": 23}
        assert mp.geometry.type == "MultiPoint"
        assert mp.geometry.coordinates == [[0, 0], [10, 10]]

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                ([[[0, 0], [1, 1]], [[2, 2]]], {"test": 23}),
                error_code_messages["InvalidMultiInput"] + "of Points",
                id="InvalidMultiInput",
            ),
            pytest.param(
                ([[0, 0], [5, "xyz"], [15, 8]], {"test": 23}),
                error_code_messages["InvalidPointInput"],
                id="InvalidPointInput",
            ),
        ],
    )
    def test_multi_point_exceptions(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            multi_point(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

    def test_to_geojson(self):

        p = point([0, 0], as_geojson=False)

        assert p.to_geojson() == {
            "geometry": {"coordinates": [0, 0], "type": "Point"},
            "properties": {},
            "type": "Feature",
        }


class TestLineString:
    def test_coordinates_props(self):

        line = line_string([[5, 10], [20, 40]], {"name": "test line"}, as_geojson=False)

        assert line.geometry.coordinates[0][0] == 5
        assert line.geometry.coordinates[1][0] == 20
        assert line.geometry.type == "LineString"
        assert line.properties["name"] == "test line"

    def test_no_props(self):

        line = line_string([[5, 10], [20, 40]], as_geojson=False)

        assert line.properties == {}

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                [[[2, 10], [1, 4]]],
                error_code_messages["InvalidLineStringInput"],
                id="InvalidLineStringInput",
            ),
            pytest.param(
                [[5, 10]],
                error_code_messages["InvalidLinePoints"],
                id="InvalidLinePoints",
            ),
            pytest.param(
                [["xyz", 10], [1, 4]],
                error_code_messages["InvalidLinePoints"],
                id="InvalidLinePoints",
            ),
        ],
    )
    def test_exceptions(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            line_string(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

    def test_line_strings(self):

        ls = line_strings(
            [
                [[-24, 63], [-23, 60], [-25, 65], [-20, 69]],
                [[-14, 43], [-13, 40], [-15, 45], [-10, 49]],
            ],
            {"foo": "bar"},
            {"id": "hello"},
            as_geojson=False,
        )

        assert len(ls.features) == 2
        assert ls.id == "hello"
        assert ls.features[0].properties["foo"] == "bar"

    def test_multi_line_string(self):

        mls = multi_line_string(
            [[[0, 0], [1, 2]], [[5, 0], [15, 8]]], {"test": 23}, as_geojson=False
        )

        assert mls.type == "Feature"
        assert mls.properties == {"test": 23}
        assert mls.geometry.type == "MultiLineString"
        assert mls.geometry.coordinates == [[[0, 0], [1, 2]], [[5, 0], [15, 8]]]

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                ([[0, 0], [5, 0], [15, 8]], {"test": 23}),
                error_code_messages["InvalidMultiInput"] + "of LineStrings",
                id="InvalidMultiInput",
            ),
            pytest.param(
                ([[[0, 0]], [[5, 0], [15, 8]]], {"test": 23}),
                error_code_messages["InvalidLinePoints"],
                id="InvalidLinePoints",
            ),
        ],
    )
    def test_multi_line_string_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            multi_line_string(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

    def test_to_geojson(self):

        line = line_string([[5, 10], [20, 40]], as_geojson=False)

        assert line.to_geojson() == {
            "geometry": {"coordinates": [[5, 10], [20, 40]], "type": "LineString"},
            "properties": {},
            "type": "Feature",
        }


class TestPolygon:
    def test_coordinates_props(self):

        poly = polygon(
            [[[5, 10], [20, 40], [40, 0], [5, 10]]],
            {"name": "test polygon"},
            as_geojson=False,
        )

        assert poly.geometry.coordinates[0][0][0] == 5
        assert poly.geometry.coordinates[0][1][0] == 20
        assert poly.geometry.coordinates[0][2][0] == 40
        assert poly.properties["name"] == "test polygon"
        assert poly.geometry.type == "Polygon"

    def test_no_props(self):

        poly = polygon([[[5, 10], [20, 40], [40, 0], [5, 10]]], as_geojson=False)

        assert poly.properties == {}

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                "xyz",
                error_code_messages["InvalidPolygonInput"],
                id="InvalidPolygonInput",
            ),
            pytest.param(
                ["xyz"],
                error_code_messages["InvalidPolygonInput"],
                id="InvalidPolygonInput",
            ),
            pytest.param(
                [[[5, 10], [20, 40], [40, 0]]],
                error_code_messages["InvalidLinearRing"],
                id="InvalidLinearRing",
            ),
            pytest.param(
                [[[5, 10], [20, 40], [40, 0], [2, 3]]],
                error_code_messages["InvalidFirstLastPoints"],
                id="InvalidFirstLastPoints",
            ),
        ],
    )
    def test_exceptions(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            polygon(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

    def test_polygons(self):

        poly = polygons(
            [
                [[[-5, 52], [-4, 56], [-2, 51], [-7, 54], [-5, 52]]],
                [[[-15, 42], [-14, 46], [-12, 41], [-17, 44], [-15, 42]]],
            ],
            {"foo": "bar"},
            {"id": "hello"},
            as_geojson=False,
        )

        assert len(poly.features) == 2
        assert poly.id == "hello"
        assert poly.features[0].properties["foo"] == "bar"

    def test_multi_polygon(self):

        mp = multi_polygon(
            [
                [[[94, 57], [78, 49], [94, 43], [94, 57]]],
                [[[93, 19], [63, 7], [79, 0], [93, 19]]],
            ],
            {"test": 23},
            as_geojson=False,
        )

        assert mp.type == "Feature"
        assert mp.properties == {"test": 23}
        assert mp.geometry.type == "MultiPolygon"
        assert mp.geometry.coordinates == [
            [[[94, 57], [78, 49], [94, 43], [94, 57]]],
            [[[93, 19], [63, 7], [79, 0], [93, 19]]],
        ]

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                (
                    [
                        [[[0, 1], [78, 49], [94, 43], [94, 57]]],
                        [[[93, 19], [63, 7], [79, 0], [93, 19]]],
                    ],
                    {"test": 23},
                ),
                error_code_messages["InvalidFirstLastPoints"],
                id="InvalidFirstLastPoints",
            ),
            pytest.param(
                (
                    [
                        [[[78, 49], [94, 43], [94, 57]]],
                        [[[93, 19], [63, 7], [79, 0], [93, 19]]],
                    ],
                    {"test": 23},
                ),
                error_code_messages["InvalidLinearRing"],
                id="InvalidLinearRing",
            ),
            pytest.param(
                ([[[93, 19], [63, 7], [79, 0], [93, 19]]], {"test": 23}),
                error_code_messages["InvalidMultiInput"] + "of Polygons",
                id="InvalidMultiInput",
            ),
        ],
    )
    def test_multi_polygon_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            multi_polygon(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

    def test_to_geojson(self):

        poly = polygon(
            [[[5, 10], [20, 40], [40, 0], [5, 10]]],
            {"name": "test polygon"},
            as_geojson=False,
        )

        assert poly.to_geojson() == {
            "geometry": {
                "coordinates": [[[5, 10], [20, 40], [40, 0], [5, 10]]],
                "type": "Polygon",
            },
            "properties": {"name": "test polygon"},
            "type": "Feature",
        }


class TestFeature:

    allowed_types = [
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
    ]

    @pytest.mark.parametrize(
        "input_value,as_geojson",
        [
            pytest.param(
                {"type": "Point", "coordinates": [4.83, 45.75]},
                True,
                id="point-geojson",
            ),
            pytest.param(Point([4.83, 45.75]), False, id="point-object",),
        ],
    )
    def test_feature(self, input_value, as_geojson):

        feat = feature(input_value, as_geojson=as_geojson)

        assert feat.get("geometry") == input_value

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                {"type": "NotGeoJSON", "coordinates": [4.83, 45.75]},
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidGeometry",
            ),
            pytest.param(
                {"type": "Point",},
                error_code_messages["InvalidCoordinates"],
                id="InvalidCoordinates",
            ),
        ],
    )
    def test_feature_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            feature(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value


class TestFeatureCollection:

    allowed_types = [
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
    ]

    @pytest.mark.parametrize(
        "input_value,as_geojson",
        [
            pytest.param(
                lambda x: [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {"type": "Point", "coordinates": [4.83, 45.75]},
                    }
                ],
                True,
                id="feature-point-geojson",
            ),
            pytest.param(
                lambda as_geojson: [
                    line_string([[4.83, 45.75], [4.94, 45.91]], as_geojson=as_geojson)
                ],
                False,
                id="feature-line_string-object",
            ),
        ],
    )
    def test_feature(self, input_value, as_geojson):

        feat_collection = feature_collection(input_value(True), as_geojson=as_geojson)

        assert feat_collection.get("features") == input_value(False)

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {"type": "Point", "coordinates": [4.83, 45.75]},
                },
                error_code_messages["InvalidFeatureCollection"],
                id="InvalidFeatureCollection",
            ),
            pytest.param(
                [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "NotGeoJSON",
                            "coordinates": [4.83, 45.75],
                        },
                    }
                ],
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidGeometryType",
            ),
            pytest.param(
                [{"type": "Point",}],
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidGeometry",
            ),
        ],
    )
    def test_feature_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            feature_collection(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value


class TestFeatureGeometry:

    allowed_types = [
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
    ]

    @pytest.mark.parametrize(
        "args,kwargs",
        [
            pytest.param(("Point", [0, 1]), {"as_geojson": True}, id="point-geojson",),
            pytest.param(
                ("LineString", [[0, 1], [2, 3]]),
                {"as_geojson": False},
                id="line_string-geojson",
            ),
            pytest.param(
                ("Polygon", [[[0, 1], [2, 3], [4, 5], [0, 1]]]),
                {"as_geojson": False},
                id="polygon-geojson",
            ),
            pytest.param(
                ("MultiPoint", [[0, 1], [2, 3]]),
                {"as_geojson": False},
                id="multi_point-geojson",
            ),
            pytest.param(
                ("MultiLineString", [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]),
                {"as_geojson": False},
                id="multi_line_string-geojson",
            ),
            pytest.param(
                (
                    "MultiPolygon",
                    [
                        [[[0, 1], [2, 3], [4, 5], [0, 1]]],
                        [[[0, 1], [2, 3], [4, 5], [0, 1]]],
                    ],
                ),
                {"as_geojson": False},
                id="multi_polygon-geojson",
            ),
        ],
    )
    def test_geometry(self, args, kwargs):

        geom = geometry(*args, **kwargs)

        assert geom.get("type") == args[0]
        assert geom.get("coordinates") == args[1]

    @pytest.mark.parametrize(
        "args,kwargs,exception_value",
        [
            pytest.param(
                ("NotGeoJSON", [0, 1]),
                {"as_geojson": True},
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidGeometryType",
            ),
            pytest.param(
                ("Point", [[0, 1]]),
                {"as_geojson": True},
                error_code_messages["InvalidPointInput"],
                id="InvalidPointInput",
            ),
            pytest.param(
                ("LineString", [[0, 1]]),
                {"as_geojson": True},
                error_code_messages["InvalidLinePoints"],
                id="InvalidLinePoints",
            ),
        ],
    )
    def test_geometry_exception(self, args, kwargs, exception_value):

        with pytest.raises(Exception) as excinfo:
            geometry(*args, **kwargs)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

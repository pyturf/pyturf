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
)
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


class TestPoint:
    def test_coordinates_props(self):

        p = point([5, 10], {"name": "test point"})

        assert p.geometry.coordinates[0] == 5
        assert p.geometry.coordinates[1] == 10
        assert p.geometry.type == "Point"
        assert p.properties["name"] == "test point"

    def test_no_props(self):

        p = point([0, 0])

        assert p.properties == {}

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                [1],
                error_code_messages["InvalidPointInput"],
                id="InvalidPointInput",
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

        pts = points([[-75, 39], [-80, 45], [-78, 50]], {"foo": "bar"}, {"id": "hello"})

        assert len(pts.features) == 3
        assert pts.id == "hello"
        assert pts.features[0].properties["foo"] == "bar"

    def test_multi_point(self):

        mp = multi_point([[0, 0], [10, 10]], {"test": 23})

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
                ([[0, 0], [5, 'xyz'], [15, 8]], {"test": 23}),
                error_code_messages["InvalidPointInput"],
                id="InvalidPointInput",
            ),
        ],
    )
    def test_multi_point_exceptions(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            multi_point(*input_value)

        assert excinfo.type == InvalidInput
        assert (
            str(excinfo.value) == exception_value
        )

    def test_to_geojson(self):

        p = point([0, 0])

        assert p.to_geojson() == {
            "geometry": {"coordinates": [0, 0], "type": "Point"},
            "properties": {},
            "type": "Feature",
        }


class TestLineString:
    def test_coordinates_props(self):

        line = line_string([[5, 10], [20, 40]], {"name": "test line"})

        assert line.geometry.coordinates[0][0] == 5
        assert line.geometry.coordinates[1][0] == 20
        assert line.geometry.type == "LineString"
        assert line.properties["name"] == "test line"

    def test_no_props(self):

        line = line_string([[5, 10], [20, 40]])

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
        )

        assert len(ls.features) == 2
        assert ls.id == "hello"
        assert ls.features[0].properties["foo"] == "bar"

    def test_multi_line_string(self):

        mls = multi_line_string([[[0, 0], [1, 2]], [[5, 0], [15, 8]]], {"test": 23})

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

        line = line_string([[5, 10], [20, 40]])

        assert line.to_geojson() == {
            "geometry": {"coordinates": [[5, 10], [20, 40]], "type": "LineString"},
            "properties": {},
            "type": "Feature",
        }


class TestPolygon:
    def test_coordinates_props(self):

        poly = polygon(
            [[[5, 10], [20, 40], [40, 0], [5, 10]]], {"name": "test polygon"}
        )

        assert poly.geometry.coordinates[0][0][0] == 5
        assert poly.geometry.coordinates[0][1][0] == 20
        assert poly.geometry.coordinates[0][2][0] == 40
        assert poly.properties["name"] == "test polygon"
        assert poly.geometry.type == "Polygon"

    def test_no_props(self):

        poly = polygon([[[5, 10], [20, 40], [40, 0], [5, 10]]])

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
            [[[5, 10], [20, 40], [40, 0], [5, 10]]], {"name": "test polygon"}
        )

        assert poly.to_geojson() == {
            "geometry": {
                "coordinates": [[[5, 10], [20, 40], [40, 0], [5, 10]]],
                "type": "Polygon",
            },
            "properties": {"name": "test polygon"},
            "type": "Feature",
        }

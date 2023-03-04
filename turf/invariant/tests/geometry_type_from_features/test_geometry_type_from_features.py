import pytest
import os

from turf.helpers import (
    point,
    line_string,
    polygon,
    feature_collection,
    Point,
    LineString,
    Polygon,
)
from turf.invariant import get_geometry_type

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)

allowed_types_default = [
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]


class TestGeometryTypeFromFeatures:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_get_geometry_type_from_features_geojson(self, fixture):
        result = get_geometry_type(fixture["in"])

        if isinstance(result, tuple):
            assert result == tuple(fixture["out"])
        else:
            assert result == fixture["out"][0]

    @pytest.mark.parametrize(
        "input_value,output_value",
        [
            pytest.param(
                point([4.83, 45.75], as_geojson=False),
                "Point",
                id="point_feature_object",
            ),
            pytest.param(
                line_string([[4.86, 45.76], [4.85, 45.74]], as_geojson=False),
                "LineString",
                id="line_string_feature_object",
            ),
            pytest.param(
                polygon(
                    [
                        [
                            [4.82, 45.79],
                            [4.88, 45.79],
                            [4.91, 45.76],
                            [4.89, 45.72],
                            [4.82, 45.71],
                            [4.77, 45.74],
                            [4.77, 45.77],
                            [4.82, 45.79],
                        ]
                    ],
                    as_geojson=False,
                ),
                "Polygon",
                id="polygon_feature_object",
            ),
            pytest.param(
                feature_collection(
                    [
                        polygon(
                            [
                                [
                                    [4.82, 45.79],
                                    [4.88, 45.79],
                                    [4.91, 45.76],
                                    [4.89, 45.72],
                                    [4.82, 45.71],
                                    [4.77, 45.74],
                                    [4.77, 45.77],
                                    [4.82, 45.79],
                                ]
                            ],
                            as_geojson=False,
                        ),
                        line_string([[4.86, 45.76], [4.85, 45.74]], as_geojson=False),
                        point([4.83, 45.75]),
                    ],
                    as_geojson=False,
                ),
                ("Polygon", "LineString", "Point"),
                id="feature_collection_object",
            ),
            pytest.param(
                Point([4.83, 45.75]),
                "Point",
                id="Point_object",
            ),
            pytest.param(
                LineString([[4.86, 45.76], [4.85, 45.74]]),
                "LineString",
                id="LineString_object",
            ),
        ],
    )
    def test_get_geometry_from_features_objects(self, input_value, output_value):
        assert get_geometry_type(input_value) == output_value

    @pytest.mark.parametrize(
        "input_value,output_value",
        [
            pytest.param(
                ([4.83, 45.75], ["Point"]),
                "Point",
                id="point_feature_object",
            ),
            pytest.param(
                ([[4.86, 45.76], [4.85, 45.74]], ["LineString"]),
                "LineString",
                id="line_string_feature_object",
            ),
            pytest.param(
                (
                    [
                        [
                            [4.82, 45.79],
                            [4.88, 45.79],
                            [4.91, 45.76],
                            [4.89, 45.72],
                            [4.82, 45.71],
                            [4.77, 45.74],
                            [4.77, 45.77],
                            [4.82, 45.79],
                        ]
                    ],
                    ["Polygon"],
                ),
                "Polygon",
                id="polygon_feature_object",
            ),
        ],
    )
    def test_get_geometry_from_lists(self, input_value, output_value):
        assert get_geometry_type(*input_value) == output_value

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                (4.83),
                error_code_messages["InvalidGeometry"](allowed_types_default),
                id="InvalidFloat",
            ),
            pytest.param(
                (4),
                error_code_messages["InvalidGeometry"](allowed_types_default),
                id="InvalidInt",
            ),
            pytest.param(
                ("4.83"),
                error_code_messages["InvalidGeometry"](allowed_types_default),
                id="InvalidString",
            ),
            pytest.param(
                (None),
                error_code_messages["InvalidGeometry"](allowed_types_default),
                id="InvalidNone",
            ),
            pytest.param(
                ({}),
                error_code_messages["InvalidGeometry"](allowed_types_default),
                id="InvalidFeaturesInput",
            ),
        ],
    )
    def test_general_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            get_geometry_type(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                (point([4.83, 45.75], as_geojson=False), ("LineString",)),
                error_code_messages["InvalidGeometry"](["LineString"]),
                id="point_vs_linestring_feature_object",
            ),
            pytest.param(
                (
                    line_string([[4.86, 45.76], [4.85, 45.74]], as_geojson=False),
                    ["Point", "MultiPoint"],
                ),
                error_code_messages["InvalidGeometry"](["Point", "MultiPoint"]),
                id="point_vs_line_string_feature_object",
            ),
            pytest.param(
                (
                    polygon(
                        [
                            [
                                [4.82, 45.79],
                                [4.88, 45.79],
                                [4.91, 45.76],
                                [4.89, 45.72],
                                [4.82, 45.71],
                                [4.77, 45.74],
                                [4.77, 45.77],
                                [4.82, 45.79],
                            ]
                        ],
                        as_geojson=False,
                    ),
                    ["Point"],
                ),
                error_code_messages["InvalidGeometry"](["Point"]),
                id="point_vs_polygon_feature_object",
            ),
            pytest.param(
                (
                    feature_collection(
                        [
                            polygon(
                                [
                                    [
                                        [4.82, 45.79],
                                        [4.88, 45.79],
                                        [4.91, 45.76],
                                        [4.89, 45.72],
                                        [4.82, 45.71],
                                        [4.77, 45.74],
                                        [4.77, 45.77],
                                        [4.82, 45.79],
                                    ]
                                ],
                                as_geojson=False,
                            ),
                            line_string(
                                [[4.86, 45.76], [4.85, 45.74]], as_geojson=False
                            ),
                            point([4.83, 45.75]),
                        ],
                        as_geojson=False,
                    ),
                    ["Polygon", "Point"],
                ),
                error_code_messages["InvalidGeometry"](["Polygon", "Point"]),
                id="one_wrong_feature_collection_object",
            ),
            pytest.param(
                (Point([4.83, 45.75]), ["MultiPoint"]),
                error_code_messages["InvalidGeometry"](["MultiPoint"]),
                id="No_Point_object",
            ),
            pytest.param(
                (LineString([[4.86, 45.76], [4.85, 45.74]]), ["MultiLineString"]),
                error_code_messages["InvalidGeometry"](["MultiLineString"]),
                id="No_LineString_object",
            ),
        ],
    )
    def test_specifid_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            get_geometry_type(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

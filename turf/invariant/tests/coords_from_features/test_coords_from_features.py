import pytest
import os

from turf.helpers import point, line_string, polygon, feature_collection
from turf.invariant import (
    get_coords_from_features,
    get_coords_from_geometry,
    get_geometry_from_features,
)

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestCoordsFromFeatures:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_get_coords_from_features_geojson(self, fixture):
        try:
            allowed_types = fixture["in"]["properties"]["allowed_types"]
        except TypeError:
            allowed_types = fixture["in"][0]
            fixture["in"] = fixture["in"][1]

        assert get_coords_from_features(fixture["in"], allowed_types) == fixture["out"]

    @pytest.mark.parametrize(
        "input_value,output_value",
        [
            pytest.param(
                (point([4.83, 45.75], as_geojson=False), ["Point"]),
                [4.83, 45.75],
                id="point_feature_object",
            ),
            pytest.param(
                (
                    line_string([[4.86, 45.76], [4.85, 45.74]], as_geojson=False),
                    ["LineString"],
                ),
                [[4.86, 45.76], [4.85, 45.74]],
                id="line_string_feature_object",
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
                    ["Polygon"],
                ),
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
                id="polygon_feature_object",
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
                    ["LineString", "Polygon", "Point"],
                ),
                [
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
                    [[4.86, 45.76], [4.85, 45.74]],
                    [4.83, 45.75],
                ],
                id="feature_collection_object",
            ),
        ],
    )
    def test_get_coords_from_features_objects(self, input_value, output_value):
        assert get_coords_from_features(*input_value) == output_value

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                (point([4.83, 45.75], as_geojson=False), ["LineString"]),
                error_code_messages["InvalidGeometry"](["LineString"]),
                id="InvalidGeometry-geojson",
            ),
            pytest.param(
                ([4.83, 45.75], ["LineString"]),
                error_code_messages["InvalidGeometry"](["LineString"]),
                id="InvalidGeometry-list",
            ),
            pytest.param(
                ([4.83], ["Point"]),
                error_code_messages["InvalidPointInput"],
                id="InvalidPoint",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            get_coords_from_features(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

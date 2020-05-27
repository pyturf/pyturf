import pytest
import os

from turf.polygon_to_line import polygon_to_line
from turf.helpers import all_geometry_types, feature_collection, point, polygon

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestPolygonToLine:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_polygon_to_line(self, fixture):

        result = polygon_to_line(fixture["in"])

        assert result == fixture["out"]

    @pytest.mark.parametrize(
        "input_value,expected_value",
        [
            pytest.param(
                (
                    polygon([[[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]]]),
                    {"properties": {"stroke": "#F00", "stroke-width": 6}},
                ),
                {
                    "type": "Feature",
                    "properties": {"stroke": "#F00", "stroke-width": 6},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]],
                    },
                },
                id="PropertiesHandling",
            )
        ],
    )
    def test_properties_handling(self, input_value, expected_value):

        result = polygon_to_line(*input_value)

        assert result == expected_value

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                (
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "coordinates": [[[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]]]
                        },
                    },
                    {},
                ),
                error_code_messages["InvalidGeometry"](("Polygon", "MultiPolygon")),
                id="InvalidPolygon",
            ),
            pytest.param(
                (
                    {"coordinates": [[[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]]]},
                    {"properties": {"stroke": "#F00", "stroke-width": 6}},
                ),
                error_code_messages["InvalidGeometry"](("Polygon", "MultiPolygon")),
                id="InvalidPolygon",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            polygon_to_line(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

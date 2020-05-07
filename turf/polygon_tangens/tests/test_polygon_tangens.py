import pytest
import os

from turf.polygon_tangens import polygon_tangens
from turf.helpers import all_geometry_types, feature_collection, point, polygon

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestPolygonTangens:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_polygon_tangens(self, fixture):

        poly = fixture["in"]["features"][0]
        pnt = fixture["in"]["features"][1]

        result = polygon_tangens(pnt, poly)

        result["features"].extend(fixture["in"]["features"])

        assert result == fixture["out"]

    def test_input_mutation_prevention(self):

        pnt = point([61, 5])
        poly = polygon(
            [[[11, 0], [22, 4], [31, 0], [31, 11], [21, 15], [11, 11], [11, 0]]]
        )
        result = polygon_tangens(pnt.get("geometry"), poly.get("geometry"))

        assert result != None

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                (point([61, 5]), point([5, 61])),
                error_code_messages["InvalidGeometry"](("Polygon", "MultiPolygon")),
                id="InvalidPolygon",
            ),
            pytest.param(
                (
                    [61, 5],
                    polygon(
                        [
                            [
                                [8.788482103824089, 51.56063487730164],
                                [8.788583, 51.561554],
                                [8.78839, 51.562241],
                                [8.78705, 51.563616],
                                [8.785483, 51.564445],
                                [8.785481, 51.564446],
                                [8.785479, 51.564447],
                                [8.785479, 51.564449],
                                [8.785478, 51.56445],
                                [8.785478, 51.564452],
                                [8.785479, 51.564454],
                                [8.78548, 51.564455],
                                [8.785482, 51.564457],
                                [8.786358, 51.565053],
                                [8.787022, 51.565767],
                                [8.787024, 51.565768],
                                [8.787026, 51.565769],
                                [8.787028, 51.56577],
                                [8.787031, 51.565771],
                                [8.787033, 51.565771],
                                [8.789951649580397, 51.56585502173034],
                                [8.789734, 51.563604],
                                [8.788482103824089, 51.56063487730164],
                            ]
                        ]
                    ),
                ),
                error_code_messages["InvalidGeometry"](all_geometry_types),
                id="InvalidGeometry",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            polygon_tangens(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

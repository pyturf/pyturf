import pytest
import os

from turf.utils.test_setup import get_fixtures
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.circle import circle

current_path = os.path.dirname(os.path.realpath(__file__))
fixtures = get_fixtures(current_path)


fixture_helpers = {
    "point_10_32_steps": [10, {"steps": 32}],
    "point_100_km": [100, {"units": "kilometers"}],
    "point_20_miles": [20, {"units": "miles"}],
}


class TestCircle:
    @pytest.mark.parametrize(
        "fixture, fixture_name",
        [
            pytest.param(fixture, fixture_name, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_circle(self, fixture, fixture_name):

        radius, options = fixture_helpers[fixture_name]

        assert circle(fixture["in"], radius, options) == fixture["out"]

    @pytest.mark.parametrize(
        "input_value, radius, exception_value",
        [
            pytest.param(
                "xyz",
                10,
                error_code_messages["InvalidGeometry"](["Point"]),
                id="InvalidGeometry",
            ),
            pytest.param(
                {
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
                },
                10,
                error_code_messages["InvalidGeometry"](["Point"]),
                id="InvalidGeometry_LineString",
            ),
            pytest.param(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                },
                "invalid_radius",
                error_code_messages["InvalidRadius"],
                id="InvalidRadius",
            ),
        ],
    )
    def test_exception(self, input_value, radius, exception_value):
        with pytest.raises(Exception) as excinfo:
            circle(input_value, radius)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

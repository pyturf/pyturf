import pytest
import os

from turf.distance import distance
from turf.point_to_line_distance import point_to_line_distance
from turf.helpers import feature_collection, point, line_string

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestPointLineDistance:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_point_to_line_distance(self, fixture):
        point = fixture["in"]["features"][0]
        line = fixture["in"]["features"][1]

        properties = fixture["in"].get("properties", {})
        options = {"units": properties.get("units", "kilometers")}

        result = {}

        for method in ["geodesic", "planar"]:
            options["method"] = method
            result[method] = round(point_to_line_distance(point, line, options), 8)

        test_result = {k: round(v, 8) for k, v in fixture["out"].items()}

        assert result == test_result

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                (point([0, 0]), line_string([[1, 1], [-1, 1]]), {"units": "foo"}),
                error_code_messages["InvalidUnits"]("foo"),
                id="InvalidUnits",
            ),
            pytest.param(
                (None, line_string([[1, 1], [-1, 1]])),
                error_code_messages["InvalidGeometry"](["Point"]),
                id="InvalidPoint",
            ),
            pytest.param(
                (point([10, 10]), None),
                error_code_messages["InvalidGeometry"](["LineString"]),
                id="InvalidLineStringInput",
            ),
            pytest.param(
                (point([10, 10]), point([10, 10])),
                error_code_messages["InvalidGeometry"](["LineString"]),
                id="InvalidLineStringInput",
            ),
            pytest.param(
                (line_string([[1, 1], [-1, 1]]), line_string([[1, 1], [-1, 1]])),
                error_code_messages["InvalidGeometry"](["Point"]),
                id="InvalidPoint",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            point_to_line_distance(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

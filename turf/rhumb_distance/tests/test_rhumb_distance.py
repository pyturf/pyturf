import pytest
import os

from turf.distance import distance
from turf.rhumb_distance import rhumb_distance
from turf.helpers import feature_collection, point

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestRhumbDistance:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_rhumb_distance(self, fixture):
        pt1 = fixture["in"]["features"][0]
        pt2 = fixture["in"]["features"][1]

        distances = {
            "miles": round(rhumb_distance(pt1, pt2, {"units": "miles"}), 6),
            "nauticalmiles": round(
                rhumb_distance(pt1, pt2, {"units": "nautical_miles"}), 6
            ),
            "kilometers": round(rhumb_distance(pt1, pt2, {"units": "kilometers"}), 6),
            "greatCircleDistance": round(
                distance(pt1, pt2, {"units": "kilometers"}), 6
            ),
            "radians": round(rhumb_distance(pt1, pt2, {"units": "radians"}), 6),
            "degrees": round(rhumb_distance(pt1, pt2, {"units": "degrees"}), 6),
        }

        assert distances == fixture["out"]

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                (point([0, 0]), point([10, 10]), {"units": "foo"}),
                error_code_messages["InvalidUnits"]("foo"),
                id="InvalidUnits",
            ),
            pytest.param(
                (None, point([10, 10])),
                error_code_messages["InvalidGeometry"](["Point"]),
                id="InvalidGeometry",
            ),
            pytest.param(
                (point([10, 10]), [10]),
                error_code_messages["InvalidPointInput"],
                id="InvalidPointInput",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            rhumb_distance(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

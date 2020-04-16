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


class TestRhumbDestination:
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

    def test_exception(self):

        wrong_units = "foo"

        with pytest.raises(Exception) as excinfo:
            rhumb_distance(point([0, 0]), point([10, 10]), {"units": wrong_units})

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == error_code_messages["InvalidUnits"](wrong_units)

        with pytest.raises(Exception) as excinfo:
            rhumb_distance(None, point([10, 10]))

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == error_code_messages["InvalidPoint"]

        with pytest.raises(Exception) as excinfo:
            rhumb_distance(point([10, 10]), "point")

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == error_code_messages["InvalidPoint"]

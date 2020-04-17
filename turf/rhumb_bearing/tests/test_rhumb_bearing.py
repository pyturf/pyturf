import pytest
import os

from turf.helpers import feature_collection, point
from turf.rhumb_bearing import rhumb_bearing

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

        initial_bearing = rhumb_bearing(pt1, pt2)
        final_bearing = rhumb_bearing(pt1, pt2, {"final": True})

        result = {
            "initialBearing": round(initial_bearing, 6),
            "finalBearing": round(final_bearing, 6),
        }

        assert result == fixture["out"]

    def test_exception(self):

        with pytest.raises(Exception) as excinfo:
            rhumb_bearing(point([10, 10]), "point")

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == error_code_messages["InvalidPoint"]

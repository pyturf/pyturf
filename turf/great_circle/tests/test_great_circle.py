import pytest
import os

from turf.great_circle import great_circle

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestGreatCircle:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_great_circle(self, fixture):
        start = fixture["in"]["features"][0]
        end = fixture["in"]["features"][1]
        properties = fixture["in"].get("properties", {})
        assert great_circle(start, end, properties) == fixture["out"]

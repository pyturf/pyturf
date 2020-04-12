import pytest
import os

from turf.destination import destination

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestDestination:

    allowed_types = ["Point"]

    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_destination(self, fixture):

        bearing = fixture["in"]["properties"].get("bearing", 180)
        dist = fixture["in"]["properties"].get("dist", 100)

        assert destination(fixture["in"], dist, bearing) == fixture["out"]

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                ([[0, 1], [2, 4]], 100, 15),
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidPoint",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            destination(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

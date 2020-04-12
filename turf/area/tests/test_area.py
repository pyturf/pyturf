import pytest
import os

from turf.area import area

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestArea:

    allowed_types = ["Polygon", "MultiPolygon"]

    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_area(self, fixture):

        assert round(area(fixture["in"])) == fixture["out"]

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                [
                    [
                        [125, -15],
                        [113, -22],
                        [117, -37],
                        [130, -33],
                        [148, -39],
                        [154, -27],
                        [144, -15],
                    ]
                ],
                error_code_messages["InvalidFirstLastPoints"],
                id="InvalidFirstLastPoints",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            area(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

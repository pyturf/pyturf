import pytest
import os

from turf.distance import distance
from turf.midpoint import midpoint

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.helpers import truncate
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path, keys=["in"])


class TestMidpoint:
    allowed_types = ["Point"]

    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_midpoint(self, fixture):
        points = fixture["in"]

        mid_point = midpoint(points[0], points[1])

        assert truncate(distance(points[0], mid_point), 2) == truncate(
            distance(points[1], mid_point), 2
        )

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                [[[1, 2], [2, 3]], [3, 4]],
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidInput-LineString",
            ),
            pytest.param(
                [[1], [2, 3]],
                error_code_messages["InvalidPointInput"],
                id="InvalidInput-Point-with-1-coordinate",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            midpoint(input_value[0], input_value[1])

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

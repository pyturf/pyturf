import pytest

from turf.helpers import point
from turf.bearing import bearing
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


class TestBearing:

    start = point([-75, 45], {"marker-color": "#F00"})
    end = point([20, 60], {"marker-color": "#00F"})

    def test_calculate_bearing(self):

        initial_bearing = bearing(self.start, self.end)

        assert round(initial_bearing, 2) == 37.75

    def test_calculate_final_bearing(self):

        final_bearing = bearing(self.start, self.end, {"final": True})

        assert round(final_bearing, 2) == 120.01

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                ([[0, 1]], [2, 3]),
                error_code_messages["InvalidPoint"],
                id="InvalidStartPoint",
            ),
            pytest.param(
                (point([0, 0]), [2, "xyz"]),
                error_code_messages["InvalidDegrees"],
                id="InvalidEndPoint",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            bearing(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

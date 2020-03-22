import pytest

from turf.helpers import point
from turf.bearing import bearing


class TestBearing:

    start = point([-75, 45], {"marker-color": "#F00"})
    end = point([20, 60], {"marker-color": "#00F"})

    def test_calculate_bearing(self):

        initial_bearing = bearing(self.start, self.end)

        assert round(initial_bearing, 2) == 37.75

    def test_calculate_final_bearing(self):

        final_bearing = bearing(self.start, self.end, {"final": True})

        assert round(final_bearing, 2) == 120.01

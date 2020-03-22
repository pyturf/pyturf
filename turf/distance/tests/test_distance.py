import pytest

from turf import point
from turf.distance.tests.fixture import fixture, expected_results
from turf.distance import distance


class TestDistance:
    @pytest.mark.parametrize(
        "units",
        [
            pytest.param("miles", id="miles"),
            pytest.param("nautical_miles", id="nautical_miles"),
            pytest.param("kilometers", id="kilometers"),
            pytest.param("radians", id="radians"),
            pytest.param("degrees", id="degrees"),
        ],
    )
    def test_distance(self, units):

        pt1 = fixture["features"][0]
        pt2 = fixture["features"][1]

        options = {"units": units}

        assert distance(pt1, pt2, options) == expected_results[units]

    def test_distance_particular(self):

        assert distance(point([-180, -90]), point([180, -90])) == 0

    def test_exception(self):

        with pytest.raises(Exception):
            distance(point([0, 0]), point([10, 10]), {"units": "foo"})

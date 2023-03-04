import pytest
import os

from turf.centroid import centroid

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestCentroid:
    allowed_types = [
        "Point",
        "MultiPoint",
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon",
    ]

    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_centroid(self, fixture):
        options = {"properties": {"marker-symbol": "circle"}}

        assert centroid(fixture["in"], options) == fixture["out"]

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                "xyz",
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidGeometry",
            ),
            pytest.param(
                [1],
                error_code_messages["InvalidPointInput"],
                id="InvalidPointInput",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            centroid(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

import pytest
import os

from turf.explode import explode

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures
from turf.helpers._features import all_geometry_types

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestExplode:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_explode(self, fixture):
        """
        # IMPORTANT! : in the original turf test cases, there were multiple
        tests with 3 dimensional coordinates [x, y, z]. In the current
        pyturf implementation only 2 dimensional coordinates are used.
        Following test cases has been changed towards 2 dimensional coordinates:
            - geometrycollection-xyz-0-6.json
            - multilinestring-xyz-0-11.json
            - multipoint-xyz-0-9.json
            - multipolygon-xyz-0-10.json
            - point-xyz-0-8.json
            - polygon-xyz-0-7.json

        """
        result = explode(fixture["in"])

        assert result == fixture["out"]

    def test_exception(self):
        with pytest.raises(Exception) as excinfo:
            explode([[1, 2]])

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == error_code_messages["InvalidGeometry"](
            all_geometry_types
        )

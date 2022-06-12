from collections import defaultdict
import pytest
import os

from turf.boolean_point_on_line import boolean_point_on_line
from turf.helpers import feature, feature_collection, point, line_string
from turf.helpers._features import all_geometry_types
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(
    current_path,
    keys=["true", "false"],
)


class TestBooleanPointOnLine:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_boolean_point_on_line(self, fixture):

        if "true" in fixture:
            features = fixture.get("true")
            point, line = features["features"]
            options = features.get("properties", {})
            expected_result = True

        else:
            features = fixture.get("false")
            point, line = features["features"]
            options = features.get("properties", {})
            expected_result = False

        test_result = boolean_point_on_line(point, line, options)

        assert test_result == expected_result

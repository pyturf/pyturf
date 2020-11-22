import pytest
import os

from turf.boolean_within import boolean_within
from turf.utils.test_setup import get_fixtures


current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path, keys=["true", "false"],)


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
            feature_1, feature_2 = features["features"]
            expected_result = True

        else:
            features = fixture.get("false")
            feature_1, feature_2 = features["features"]
            expected_result = False

        test_result = boolean_within(feature_1, feature_2)

        assert test_result == expected_result

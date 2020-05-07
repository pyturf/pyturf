import pytest
import os

from turf.point_on_feature import point_on_feature
from turf.helpers import feature, feature_collection, point, line_string
from turf.helpers._features import all_geometry_types
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestPointLineDistance:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_point_to_line_distance(self, fixture):

        point = point_on_feature(fixture["in"])
        test_result = prepare_response(point, fixture["in"])

        assert test_result == fixture["out"]


def prepare_response(point, fixture_in):

    point["properties"]["marker-color"] = "#F00"
    point["properties"]["marker-style"] = "star"
    point["properties"].pop("featureIndex", None)
    point["properties"].pop("distanceToPoint", None)

    fixture_in_type = fixture_in.get("type")

    if fixture_in_type == "Feature":
        fixture_in = feature_collection([fixture_in, point])

    elif fixture_in_type == "FeatureCollection":
        fixture_in["features"].append(point)

    else:
        fixture_in = feature_collection([feature(fixture_in), point])

    return fixture_in

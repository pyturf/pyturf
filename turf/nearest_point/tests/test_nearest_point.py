import pytest
import os

from turf.nearest_point import nearest_point

from turf.helpers import feature_collection, point
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path, keys=["in", "out"])


class TestNearestPoint:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_nearest_point(self, fixture):
        target_point = point(fixture["in"]["properties"]["targetPoint"])
        result = nearest_point(target_point, fixture["in"])

        result = prepare_response(result, target_point, fixture["in"])

        assert result == fixture["out"]

    def test_input_mutation(self):
        point_1 = point([40, 50], {"featureIndex": "foo"})
        point_2 = point([20, -10], {"distanceToPoint": "bar"})
        points = feature_collection([point_1, point_2])

        result = nearest_point([0, 0], points)

        # Check if featureIndex properties was added to properties
        assert result["properties"]["featureIndex"] == 1

        # Check if previous input points have been modified
        assert point_1["properties"] == {"featureIndex": "foo"}
        assert point_2["properties"] == {"distanceToPoint": "bar"}


def prepare_response(nearest_point, target_point, fixture_in):
    nearest_point["properties"].update(
        {"marker-color": "#F00", "marker-symbol": "star"}
    )

    target_point["properties"].update(
        {"marker-color": "#00F", "marker-symbol": "circle"}
    )

    result = feature_collection([*fixture_in["features"], target_point, nearest_point])

    return result

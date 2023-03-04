from copy import deepcopy
import pytest
import os

from turf.line_intersect import line_intersect
from turf.helpers import all_geometry_types, feature_collection, line_string, polygon

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestLineIntersectss:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_line_intersect(self, fixture):
        line_1 = fixture["in"]["features"][0]
        line_2 = fixture["in"]["features"][1]

        result = line_intersect(line_1, line_2)

        assert result.keys() == fixture["out"].keys()
        assert len(result["features"]) == len(fixture["out"]["features"])
        assert (
            all([i in result["features"] for i in fixture["out"]["features"]]) == True
        )
        assert (
            all([i in fixture["out"]["features"] for i in result["features"]]) == True
        )

    def test_input_mutation_prevention(self):
        line_1 = line_string([[7, 50], [8, 50], [9, 50]])
        line_2 = line_string([[8, 49], [8, 50], [8, 51]])

        line_1_cpy = deepcopy(line_1)
        line_2_cpy = deepcopy(line_2)

        _ = line_intersect(line_1, line_2)

        assert line_1 == line_1_cpy
        assert line_2 == line_2_cpy

    @pytest.mark.parametrize(
        "input_value,expected_value",
        [
            pytest.param(
                (
                    line_string([[7, 50], [8, 50], [9, 50]])["geometry"],
                    line_string([[8, 49], [8, 50], [8, 51]])["geometry"],
                ),
                [8, 50],
                id="ListHandling",
            ),
            pytest.param(
                (
                    feature_collection(
                        [line_string([[7, 50], [8, 50], [9, 50], [7, 50]])]
                    ),
                    feature_collection(
                        [line_string([[8, 49], [8, 50], [8, 51], [8, 49]])]
                    ),
                ),
                [8, 50],
                id="FeatureCollectionHandling",
            ),
            pytest.param(
                (
                    polygon([[[7, 50], [8, 50], [9, 50], [7, 50]]]),
                    polygon([[[8, 49], [8, 50], [8, 51], [8, 49]]]),
                ),
                [8, 50],
                id="PolygonHandling",
            ),
        ],
    )
    def test_geometric_objects(self, input_value, expected_value):
        result = line_intersect(*input_value)

        assert result["features"][0]["geometry"]["coordinates"] == expected_value

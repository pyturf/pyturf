import pytest
import os

from turf.helpers import line_string, feature_collection
from turf.invariant import get_coords_from_features
from turf.rhumb_destination import rhumb_destination

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestRhumbDestination:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_rhumb_destination(self, fixture):

        destination_point = rhumb_destination(fixture["in"])

        test_result = prepare_response(destination_point, fixture["in"])

        assert test_result == fixture["out"]


def prepare_response(destination_point, fixture_in):

    coords = get_coords_from_features(fixture_in)
    coords = [round(coord, 6) for coord in coords]

    dest_coords = get_coords_from_features(destination_point)
    dest_coords = [round(coord, 6) for coord in dest_coords]

    line = line_string([coords, dest_coords], {"stroke": "#F00", "stroke-width": 4})

    fixture_in["properties"]["marker-color"] = "#F00"

    result = feature_collection([line, fixture_in, destination_point])

    return result

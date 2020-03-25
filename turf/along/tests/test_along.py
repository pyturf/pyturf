import pytest
import json
import os
from collections import defaultdict

from turf.helpers import point
from turf.along import along

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput

current_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(os.path.join(current_path, "in"), "dc-line.geojson"), "r") as f:
    line_string_fixture = json.load(f)

fixtures = defaultdict(lambda: {"in": line_string_fixture, "out": None})

for key in ["out"]:

    files_path = os.path.join(current_path, key)

    for filename in os.listdir(files_path):
        with open(os.path.join(files_path, filename), "r") as f:
            name = ".".join(filename.split(".")[:-1])
            print(filename)
            fixtures[name][key] = json.load(f)


class TestAlong:

    allowed_types = ["LineString"]

    @pytest.mark.parametrize(
        "fixture,fixture_name",
        [
            pytest.param(fixture, fixture_name, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_along(self, fixture, fixture_name):

        distance = float(fixture_name.split("-")[1])

        print(distance)

        assert along(fixture["in"], distance) == fixture["out"]

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                (point([0, 1]), 1, 15),
                error_code_messages["InvalidGeometry"](allowed_types),
                id="InvalidPoint",
            ),
            pytest.param(
                ([[0, 1], [2, 3]], -10),
                error_code_messages["InvalidDistance"],
                id="InvalidDistance",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            along(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

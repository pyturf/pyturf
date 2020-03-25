import pytest
import json
import os
from collections import defaultdict

from turf.helpers import point
from turf.destination import destination

# TODO: make this test set up a function
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = defaultdict(lambda: {"in": None, "out": None})

for key in ["in", "out"]:

    files_path = os.path.join(current_path, key)

    for filename in os.listdir(files_path):
        with open(os.path.join(files_path, filename), "r") as f:
            name = filename.split(".")[0]
            fixtures[name][key] = json.load(f)


class TestDestination:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_destination(self, fixture):

        bearing = fixture["in"]["properties"].get("bearing", 180)
        dist = fixture["in"]["properties"].get("dist", 100)

        assert destination(fixture["in"], dist, bearing) == fixture["out"]

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(([[0, 1], [2, 4]], 100, 15), error_code_messages["InvalidPoint"], id="InvalidPoint"),
            pytest.param((point([0, 0]), -100, 0), error_code_messages["InvalidDistance"], id="InvalidDistance"),
        ]
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            destination(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

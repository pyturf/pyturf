import pytest
import os
import json
from collections import defaultdict

from turf.helpers import point, multi_line_string
from turf.length import length

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = defaultdict(lambda: {"in": None, "out": None})

for key in ["in", "out"]:

    files_path = os.path.join(current_path, key)

    for filename in os.listdir(files_path):
        with open(os.path.join(files_path, filename), "r") as f:
            name = filename.split(".")[0]
            fixtures[name][key] = json.load(f)


class TestLength:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_length(self, fixture):

        assert round(length(fixture["in"], {"units": "feet"})) == fixture["out"]

    def test_length_with_feature_classes(self):

        feature = multi_line_string([[
            [-77.031669, 38.878605],
            [-77.029609, 38.881946],
            [-77.020339, 38.884084],
            [-77.025661, 38.885821],
            [-77.021884, 38.889563],
            [-77.019824, 38.892368]
        ], [
            [-77.041669, 38.885821],
            [-77.039609, 38.881946],
            [-77.030339, 38.884084],
            [-77.035661, 38.878605]]
        ])

        assert round(length(feature, {"units": "feet"})) == 15433

    def test_exception(self):

        with pytest.raises(Exception) as excinfo:
            length([0, 0])
        assert "Input must be" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            length(point([0, 0]))
        assert "Input must be" in str(excinfo.value)

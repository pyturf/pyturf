import pytest
import os
import json
from collections import defaultdict

from turf.helpers import point, multi_line_string
from turf.utils.exceptions import InvalidInput
from turf.utils.error_codes import error_code_messages
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

    allowed_inpuy_types = [
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon",
    ]

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

        feature = multi_line_string(
            [
                [
                    [-77.031669, 38.878605],
                    [-77.029609, 38.881946],
                    [-77.020339, 38.884084],
                    [-77.025661, 38.885821],
                    [-77.021884, 38.889563],
                    [-77.019824, 38.892368],
                ],
                [
                    [-77.041669, 38.885821],
                    [-77.039609, 38.881946],
                    [-77.030339, 38.884084],
                    [-77.035661, 38.878605],
                ],
            ]
        )

        assert round(length(feature, {"units": "feet"})) == 15433

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                [0, 0],
                error_code_messages["InvalidGeometry"](allowed_inpuy_types),
                id="InvalidGeometry",
            ),
            pytest.param(
                point([0, 0]),
                error_code_messages["InvalidGeometry"](allowed_inpuy_types),
                id="InvalidGeometry",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            length(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

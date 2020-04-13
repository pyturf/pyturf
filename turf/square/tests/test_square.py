import pytest
import os

from turf.square import square

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.helpers import line_string


class TestSquare:
    @pytest.mark.parametrize(
        "bbox,result",
        [
            pytest.param([0, 0, 5, 10], [-2.5, 0, 7.5, 10]),
            pytest.param([0, 0, 10, 5], [0, -2.5, 10, 7.5]),
            pytest.param([0, 0, 10, 10], [0, 0, 10, 10]),
        ],
    )
    def test_square(self, bbox, result):

        squared_bbox = square(bbox)

        assert squared_bbox == result

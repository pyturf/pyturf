import pytest
import os

from turf.great_circle._arc import GreatCircle

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.helpers import line_string


class TestArc:
    @pytest.mark.parametrize(
        "arc,npoints,distance",
        [
            pytest.param([[0, 0], [1, 1]], 2, 0.025, id="2-points-arc",),
            pytest.param(
                [[0, 0], [0.499962, 0.500019], [1, 1]], 3, 0.025, id="3-points-arc",
            ),
            # """https://rdrr.io/cran/geosphere/man/intermediate.html"""
            pytest.param(
                [
                    [5, 52],
                    [-9.924971, 59.600848],
                    [-31.666402, 64.654693],
                    [-58.557896, 65.517701],
                    [-82.746574, 61.800954],
                    [-99.938739, 54.937003],
                    [-111.623334, 46.397464],
                    [-120, 37],
                ],
                8,
                1.377,
                id="8-points-arc",
            ),
        ],
    )
    def test_intermediate_points(self, arc, npoints, distance):

        gc = GreatCircle(arc[0], arc[-1], {"npoints": npoints})

        assert gc.properties == {"npoints": npoints}
        assert gc.arc_coordinates == arc
        assert round(gc.distance, 3) == distance

    def test_antipodal(self):

        with pytest.raises(InvalidInput):
            GreatCircle([0, 0], [180, 0], {})

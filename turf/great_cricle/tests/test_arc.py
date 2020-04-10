import pytest
import os

from turf.great_cricle._arc import GreatCircle

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.helpers import line_string



class TestGreatCircle:

    def test_great_circle(self):

        arc = [[0.00000, 0.00000],
               [1.00000, 1.00000]]

        great_circle = GreatCircle([0, 0], [1, 1], {})

        assert great_circle.properties == {}
        assert great_circle.arc_coordinates == arc
        assert round(great_circle.distance,3) == 0.025


class TestGreatCircleIntermediate:

    def test_great_circle(self):

        arc = [[0, 0],
               [0.499962, 0.500019],
               [1, 1]]

        great_circle = GreatCircle([0, 0], [1, 1], {"npoints": 1})

        assert great_circle.properties == {"npoints": 1}
        assert great_circle.arc_coordinates == arc
        assert round(great_circle.distance,3) == 0.025


class TestGreatCircleMoreIntermediate:
    """https://rdrr.io/cran/geosphere/man/intermediate.html"""
    def test_great_circle(self):

        arc = [[5, 52], [-9.924971, 59.600848],
               [-31.666402, 64.654693], [-58.557896, 65.517701],
               [-82.746574, 61.800954], [-99.938739, 54.937003],
               [-111.623334, 46.397464], [-120, 37]]

        great_circle = GreatCircle([5, 52], [-120, 37], {"npoints": 6})

        assert great_circle.properties == {"npoints": 6}
        assert great_circle.arc_coordinates == arc
        assert round(great_circle.distance,3) == 1.377


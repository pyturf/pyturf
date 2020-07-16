import pytest
import os

from turf.helpers import polygon, point
from turf.boolean_point_in_polygon import boolean_point_in_polygon

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path, keys=["in"])


class TestBooleanPointInPolygon:

    allowed_types_polygon = [
        "Polygon",
        "MultiPolygon",
    ]

    @pytest.mark.parametrize(
        "fixture,points",
        [
            pytest.param(
                fixtures["poly-with-hole"],
                [
                    (point([-86.69208526611328, 36.20373274711739]), False),
                    (point([-86.72229766845702, 36.20258997094334]), True),
                    (point([-86.75079345703125, 36.18527313913089]), False),
                ],
                id="poly-with-hole",
            ),
            pytest.param(
                fixtures["multipoly-with-hole"],
                [
                    (point([-86.69208526611328, 36.20373274711739]), False),
                    (point([-86.72229766845702, 36.20258997094334]), True),
                    (point([-86.75079345703125, 36.18527313913089]), True),
                    (point([-86.75302505493164, 36.23015046460186]), False),
                ],
                id="multipoly-with-hole",
            ),
        ],
    )
    def test_boolean_point_in_polygon(self, fixture, points):

        poly = fixture["in"]

        for pt, result in points:
            assert boolean_point_in_polygon(pt, poly) is result

    @pytest.mark.parametrize(
        "poly,point_in,point_out",
        [
            pytest.param(
                polygon([[[0, 0], [0, 100], [100, 100], [100, 0], [0, 0]]]),
                point([50, 50]),
                point([140, 150]),
                id="simple_polygon",
            ),
            pytest.param(
                polygon([[[0, 0], [50, 50], [0, 100], [100, 100], [100, 0], [0, 0]]]),
                point([75, 75]),
                point([25, 50]),
                id="concave_polygon",
            ),
        ],
    )
    def test_boolean_point_in_polygon_simple(self, poly, point_in, point_out):

        assert boolean_point_in_polygon(point_in, poly)
        assert not boolean_point_in_polygon(point_out, poly)

    @pytest.mark.parametrize(
        "poly,points",
        [
            pytest.param(
                polygon([[[10, 10], [30, 20], [50, 10], [30, 0], [10, 10]]]),
                [
                    [point([10, 10]), lambda ignore_boundary: ignore_boundary is False],
                    [point([30, 20]), lambda ignore_boundary: ignore_boundary is False],
                    [point([50, 10]), lambda ignore_boundary: ignore_boundary is False],
                    [point([30, 10]), lambda ignore_boundary: True],
                    [point([0, 10]), lambda ignore_boundary: False],
                    [point([60, 10]), lambda ignore_boundary: False],
                    [point([30, -10]), lambda ignore_boundary: False],
                    [point([30, 30]), lambda ignore_boundary: False],
                ],
                id="poly-1",
            ),
            pytest.param(
                polygon([[[10, 0], [30, 20], [50, 0], [30, 10], [10, 0]]]),
                [
                    [point([30, 0]), lambda ignore_boundary: False],
                    [point([0, 0]), lambda ignore_boundary: False],
                    [point([60, 0]), lambda ignore_boundary: False],
                ],
                id="poly-2",
            ),
            pytest.param(
                polygon([[[10, 0], [30, 20], [50, 0], [30, -20], [10, 0]]]),
                [
                    [point([30, 0]), lambda ignore_boundary: True],
                    [point([0, 0]), lambda ignore_boundary: False],
                    [point([60, 0]), lambda ignore_boundary: False],
                ],
                id="poly-3",
            ),
            pytest.param(
                polygon(
                    [
                        [
                            [0, 0],
                            [0, 20],
                            [50, 20],
                            [50, 0],
                            [40, 0],
                            [30, 10],
                            [30, 0],
                            [20, 10],
                            [10, 10],
                            [10, 0],
                            [0, 0],
                        ]
                    ]
                ),
                [
                    [point([0, 20]), lambda ignore_boundary: ignore_boundary is False],
                    [point([10, 20]), lambda ignore_boundary: ignore_boundary is False],
                    [point([50, 20]), lambda ignore_boundary: ignore_boundary is False],
                    [point([0, 10]), lambda ignore_boundary: ignore_boundary is False],
                    [point([5, 10]), lambda ignore_boundary: True],
                    [point([25, 10]), lambda ignore_boundary: True],
                    [point([35, 10]), lambda ignore_boundary: True],
                    [point([0, 0]), lambda ignore_boundary: ignore_boundary is False],
                    [point([20, 0]), lambda ignore_boundary: False],
                    [point([35, 0]), lambda ignore_boundary: False],
                    [point([50, 0]), lambda ignore_boundary: ignore_boundary is False],
                    [point([50, 10]), lambda ignore_boundary: ignore_boundary is False],
                    [point([5, 0]), lambda ignore_boundary: ignore_boundary is False],
                    [point([10, 0]), lambda ignore_boundary: ignore_boundary is False],
                ],
                id="poly-4",
            ),
            pytest.param(
                polygon(
                    [
                        [[0, 20], [20, 40], [40, 20], [20, 0], [0, 20]],
                        [[10, 20], [20, 30], [30, 20], [20, 10], [10, 20]],
                    ]
                ),
                [
                    [point([20, 30]), lambda ignore_boundary: ignore_boundary is False],
                    [point([25, 25]), lambda ignore_boundary: ignore_boundary is False],
                    [point([30, 20]), lambda ignore_boundary: ignore_boundary is False],
                    [point([25, 15]), lambda ignore_boundary: ignore_boundary is False],
                    [point([20, 10]), lambda ignore_boundary: ignore_boundary is False],
                    [point([15, 15]), lambda ignore_boundary: ignore_boundary is False],
                    [point([10, 20]), lambda ignore_boundary: ignore_boundary is False],
                    [point([15, 25]), lambda ignore_boundary: ignore_boundary is False],
                    [point([20, 20]), lambda ignore_boundary: False],
                ],
                id="poly-5",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "boundary",
        [
            pytest.param(True, id="include-boundary"),
            pytest.param(False, id="ignore-boundary"),
        ],
    )
    def test_boolean_point_in_polygon_boundary(self, boundary, poly, points):

        options = {"ignoreBoundary": boundary}

        for pt, result in points:
            assert boolean_point_in_polygon(pt, poly, options) is result(boundary)

    @pytest.mark.parametrize(
        "pt,poly,exception_value",
        [
            pytest.param(
                "xyz",
                polygon([[[10, 0], [30, 20], [50, 0], [30, 10], [10, 0]]]),
                error_code_messages["InvalidGeometry"](["Point"]),
                id="InvalidGeometry",
            ),
            pytest.param(
                point([0, 1]),
                "",
                error_code_messages["InvalidGeometry"](allowed_types_polygon),
                id="InvalidGeometry",
            ),
            pytest.param(
                point([0, 1]),
                [[0, 1], [1, 2], [2, 3], [0, 1]],
                error_code_messages["InvalidGeometry"](allowed_types_polygon),
                id="InvalidGeometry-input_must_have_a_geometry",
            ),
        ],
    )
    def test_exception(self, pt, poly, exception_value):

        with pytest.raises(Exception) as excinfo:
            boolean_point_in_polygon(pt, poly)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

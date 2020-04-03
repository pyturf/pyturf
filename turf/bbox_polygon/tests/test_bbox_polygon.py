import pytest
import os

from turf.bbox_polygon import bbox_polygon
from turf.invariant import get_coords_from_features

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestBBoxPolygon:

    allowed_types = [
        "Point",
        "MultiPoint",
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
    def test_bbox_polygon(self, fixture):

        polygon = bbox_polygon(fixture["in"])

        assert polygon == fixture["out"]

        coordinates = get_coords_from_features(polygon)

        assert len(coordinates[0]) == 5
        assert coordinates[0][0][0] == coordinates[0][len(coordinates) - 1][0]
        assert coordinates[0][0][1] == coordinates[0][len(coordinates) - 1][1]

    @pytest.mark.parametrize(
        "input_value, exception_value",
        [
            pytest.param(
                "xyz",
                error_code_messages["InvalidBoundingBox"],
                id="InvalidBoundingBox",
            ),
            pytest.param(
                [-110, 70, 5000, 50, 60, 3000],
                error_code_messages["InvalidBoundingBox"],
                id="InvalidBoundingBox",
            ),
        ],
    )
    def test_exception(self, input_value, exception_value):

        with pytest.raises(Exception) as excinfo:
            bbox_polygon(input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

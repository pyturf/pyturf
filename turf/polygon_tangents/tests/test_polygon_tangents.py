import pytest
import os

from turf.polygon_tangents import polygon_tangents
from turf.helpers import all_geometry_types, feature_collection, point, polygon

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestPolygonTangents:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_polygon_tangens(self, fixture):
        poly = fixture["in"]["features"][0]
        pnt = fixture["in"]["features"][1]

        result = polygon_tangents(pnt, poly)

        result["features"].extend(fixture["in"]["features"])

        assert result == fixture["out"]

    def test_input_mutation_prevention(self):
        pnt = point([61, 5])
        poly = polygon(
            [[[11, 0], [22, 4], [31, 0], [31, 11], [21, 15], [11, 11], [11, 0]]]
        )
        result = polygon_tangents(pnt.get("geometry"), poly.get("geometry"))

        assert result != None

    @pytest.mark.parametrize(
        "input_value,exception_value",
        [
            pytest.param(
                (point([61, 5]), point([5, 61])),
                error_code_messages["InvalidGeometry"](("Polygon", "MultiPolygon")),
                id="InvalidPolygon",
            )
        ],
    )
    def test_exception(self, input_value, exception_value):
        with pytest.raises(Exception) as excinfo:
            polygon_tangents(*input_value)

        assert excinfo.type == InvalidInput
        assert str(excinfo.value) == exception_value

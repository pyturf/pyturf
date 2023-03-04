import pytest
from math import pi

from turf.helpers._units import earth_radius
from turf.helpers import (
    radians_to_length,
    length_to_radians,
    length_to_degrees,
    radians_to_degrees,
    degrees_to_radians,
    convert_length,
    convert_area,
)


@pytest.mark.parametrize(
    "value,units,result",
    [
        (1, "radians", 1),
        (1, "kilometers", earth_radius / 1000),
        (1, "miles", earth_radius / 1609.344),
    ],
)
def test_radians_to_length(value, units, result):
    assert radians_to_length(value, units) == result


@pytest.mark.parametrize(
    "value,units,result",
    [
        (1, "radians", 1),
        (earth_radius / 1000, "kilometers", 1),
        (earth_radius / 1609.344, "miles", 1),
    ],
)
def test_length_to_radians(value, units, result):
    assert length_to_radians(value, units) == result


@pytest.mark.parametrize(
    "value,units,result",
    [
        (1, "radians", 57.29577951308232),
        (100, "kilometers", 0.899320363724538),
        (10, "miles", 0.1447315831437903),
    ],
)
def test_length_to_degrees(value, units, result):
    assert length_to_degrees(value, units) == result


@pytest.mark.parametrize(
    "value,result",
    [
        pytest.param(pi / 3, 60, id="radiance conversion PI/3"),
        pytest.param(3.5 * pi, 270, id="radiance conversion 3.5 PI"),
        pytest.param(-1 * pi, -180, id="radiance conversion -PI"),
    ],
)
def test_radians_to_degrees(value, result):
    assert round(radians_to_degrees(value), 6) == result


@pytest.mark.parametrize(
    "value,result",
    [
        pytest.param(60, pi / 3, id="degrees conversion 60"),
        pytest.param(270, 1.5 * pi, id="degrees conversion 270"),
        pytest.param(-180, -pi, id="degrees conversion -180"),
    ],
)
def test_degrees_to_radians(value, result):
    assert degrees_to_radians(value) == result


@pytest.mark.parametrize(
    "value,original_unit,final_unit,result",
    [
        pytest.param(1000, "meters", "kilometers", 1),
        pytest.param(1, "kilometers", "miles", 0.621371192237334),
        pytest.param(1, "miles", "kilometers", 1.609344),
        pytest.param(1, "nautical_miles", "kilometers", 1.852),
        pytest.param(1, "meters", "centimeters", 100.00000000000001),
    ],
)
def test_convert_length(value, original_unit, final_unit, result):
    assert convert_length(value, original_unit, final_unit) == result


@pytest.mark.parametrize(
    "value,original_unit,final_unit,result",
    [
        pytest.param(1000, "meters", "kilometers", 0.001),
        pytest.param(1, "kilometres", "miles", 0.386),
        pytest.param(1, "miles", "kilometers", 2.5906735751295336),
        pytest.param(1, "meters", "centimetres", 10000),
        pytest.param(100, "metres", "acres", 0.0247105),
        pytest.param(100, "metres", "yards", 119.59900459999999),
        pytest.param(100, "metres", "feet", 1076.3910417),
        pytest.param(100000, "feet", "kilometers", 0.009290303999749462),
    ],
)
def test_convert_area(value, original_unit, final_unit, result):
    assert convert_area(value, original_unit, final_unit) == result

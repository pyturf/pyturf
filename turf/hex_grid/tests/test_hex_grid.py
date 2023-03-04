import pytest
import os

from turf.bbox_polygon import bbox_polygon
from turf.hex_grid import hex_grid

from turf.utils.test_setup import get_fixtures


current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestHexGrid:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_hex_grid(self, fixture):
        bbox = fixture["in"]["bbox"]
        n_cells = fixture["in"]["cellSide"]

        options = dict(
            (key, fixture["in"][key])
            for key in ["units", "mask", "properties", "triangles"]
            if key in fixture["in"]
        )

        result = hex_grid(bbox, n_cells, options)

        result = prepare_output(result, bbox, options)

        assert result == fixture["out"]

    @pytest.mark.parametrize(
        "input_value,expected_value",
        [
            pytest.param(
                (
                    [
                        -96.6357421875,
                        31.12819929911196,
                        -84.9462890625,
                        40.58058466412764,
                    ],
                    50,
                    {"units": "miles"},
                ),
                52,
                id="GridTilesCounting",
            ),
            pytest.param(
                (
                    [
                        -96.6357421875,
                        31.12819929911196,
                        -84.9462890625,
                        40.58058466412764,
                    ],
                    50,
                    {"units": "miles", "triangles": True},
                ),
                312,
                id="GridTilesCountingTriangles",
            ),
        ],
    )
    def test_grid_tiles_count(self, input_value, expected_value):
        result = hex_grid(*input_value)

        assert len(result["features"]) == expected_value

    @pytest.mark.parametrize(
        "input_value,expected_value",
        [
            pytest.param(
                (
                    [
                        -96.6357421875,
                        31.12819929911196,
                        -84.9462890625,
                        40.58058466412764,
                    ],
                    50,
                    {"units": "miles", "properties": {"foo": "bar"}},
                ),
                ("bar", "bar", "baz", "bar"),
                id="Property mutation",
            )
        ],
    )
    def test_property_mutation(self, input_value, expected_value):
        result = hex_grid(*input_value)

        assert result["features"][0]["properties"]["foo"] == expected_value[0]
        assert result["features"][1]["properties"]["foo"] == expected_value[1]

        result["features"][0]["properties"]["foo"] = "baz"

        assert result["features"][0]["properties"]["foo"] == expected_value[2]
        assert result["features"][1]["properties"]["foo"] == expected_value[3]

    @pytest.mark.parametrize(
        "input_value,expected_value",
        [
            pytest.param(
                (
                    [-179, -90, 179, 90],
                    250,
                    {"units": "kilometers"},
                ),
                (1000, -1000),
                id="longitude (13141439571036224) - issue #758",
            )
        ],
    )
    def test_longitude_issue_758(self, input_value, expected_value):
        result = hex_grid(*input_value)

        coords = []
        for feature in result["features"]:
            for hex in feature["geometry"]["coordinates"]:
                for coord in hex:
                    coords.append(coord)

        for coord in coords:
            assert coord[0] <= expected_value[0]
            assert coord[1] >= expected_value[1]


def prepare_output(result, bbox, options):
    for i in range(len(result["features"])):
        coords = round_coordinates(result["features"][i])
        result["features"][i] = coords

    bbox_poly = bbox_polygon(bbox)
    bbox_poly["properties"] = {"stroke": "#F00", "stroke-width": 6, "fill-opacity": 0}

    result["features"].append(bbox_poly)

    if "mask" in options:
        options["mask"]["properties"] = {
            "stroke": "#00F",
            "stroke-width": 6,
            "fill-opacity": 0,
        }
        result["features"].append(options["mask"])

    return result


def round_coordinates(cell_poly):
    """
    Rounds the coords of the polygon
    Only implemented to pass tests.

    :param cell_poly: polygon feature

    :returns: polygon feature
    """

    coords = cell_poly["geometry"]["coordinates"]

    coords = [
        [[round(coord, 6) for coord in point] for point in line] for line in coords
    ]

    cell_poly["geometry"]["coordinates"] = coords

    return cell_poly

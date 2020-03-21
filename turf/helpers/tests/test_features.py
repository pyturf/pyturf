import pytest

from turf.helpers._features import (
    point,
    line_string,
    polygon,
    points,
    line_strings,
    polygons,
    multi_point,
    multi_line_string,
    multi_polygon,
)


class TestPoint:
    def test_coordinates_props(self):

        p = point([5, 10], {"name": "test point"})

        assert p.geometry.coordinates[0] == 5
        assert p.geometry.coordinates[1] == 10
        assert p.geometry.type == "Point"
        assert p.properties["name"] == "test point"

    def test_no_props(self):

        p = point([0, 0])

        assert p.properties == {}

    def test_exceptions(self):

        with pytest.raises(Exception):
            point()

        with pytest.raises(Exception) as excinfo:
            point([1])
        assert "[lng, lat]" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            point([1, "xyz"])
        assert "invalid" in str(excinfo.value)

    def test_points(self):

        pts = points([[-75, 39], [-80, 45], [-78, 50]], {"foo": "bar"}, {"id": "hello"})

        assert len(pts.features) == 3
        assert pts.id == "hello"
        assert pts.features[0].properties["foo"] == "bar"

    def test_multi_point(self):

        mp = multi_point([[0, 0], [10, 10]], {"test": 23})

        assert mp.type == "Feature"
        assert mp.properties == {"test": 23}
        assert mp.geometry.type == "MultiPoint"
        assert mp.geometry.coordinates == [[0, 0], [10, 10]]


class TestLineString:
    def test_coordinates_props(self):

        line = line_string([[5, 10], [20, 40]], {"name": "test line"})

        assert line.geometry.coordinates[0][0] == 5
        assert line.geometry.coordinates[1][0] == 20
        assert line.geometry.type == "LineString"
        assert line.properties["name"] == "test line"

    def test_no_props(self):

        line = line_string([[5, 10], [20, 40]])

        assert line.properties == {}

    def test_exceptions(self):

        with pytest.raises(Exception):
            line_string()

        with pytest.raises(Exception) as excinfo:
            line_string([[5, 10]])
        assert "two or more" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            line_string([["xyz", 10], [1, 4]])
        assert "invalid" in str(excinfo.value)

    def test_line_strings(self):

        ls = line_strings(
            [
                [[-24, 63], [-23, 60], [-25, 65], [-20, 69]],
                [[-14, 43], [-13, 40], [-15, 45], [-10, 49]],
            ],
            {"foo": "bar"},
            {"id": "hello"},
        )

        assert len(ls.features) == 2
        assert ls.id == "hello"
        assert ls.features[0].properties["foo"] == "bar"

    def test_multi_line_string(self):

        mls = multi_line_string([[[0, 0], [1, 2]], [[5, 0], [15, 8]]], {"test": 23})

        assert mls.type == "Feature"
        assert mls.properties == {"test": 23}
        assert mls.geometry.type == "MultiLineString"
        assert mls.geometry.coordinates == [[[0, 0], [1, 2]], [[5, 0], [15, 8]]]

    def test_multi_line_string_exception(self):

        with pytest.raises(Exception) as excinfo:
            multi_line_string([[[0, 0]], [[5, 0], [15, 8]]], {"test": 23})
        assert "two or more" in str(excinfo.value)


class TestPolygon:
    def test_coordinates_props(self):

        poly = polygon(
            [[[5, 10], [20, 40], [40, 0], [5, 10]]], {"name": "test polygon"}
        )

        assert poly.geometry.coordinates[0][0][0] == 5
        assert poly.geometry.coordinates[0][1][0] == 20
        assert poly.geometry.coordinates[0][2][0] == 40
        assert poly.properties["name"] == "test polygon"
        assert poly.geometry.type == "Polygon"

    def test_no_props(self):

        poly = polygon([[[5, 10], [20, 40], [40, 0], [5, 10]]])

        assert poly.properties == {}

    def test_exceptions(self):

        with pytest.raises(Exception):
            polygon()

        with pytest.raises(Exception) as excinfo:
            polygon("xyz")
        assert "list of LinearRing" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            polygon(["xyz"])
        assert "list of Positions" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            polygon([[[5, 10], [20, 40], [40, 0]]])
        assert "4 or more Positions" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            polygon([[[5, 10], [20, 40], [40, 0], [2, 3]]])
        assert "not equivalent" in str(excinfo.value)

    def test_polygons(self):

        poly = polygons(
            [
                [[[-5, 52], [-4, 56], [-2, 51], [-7, 54], [-5, 52]]],
                [[[-15, 42], [-14, 46], [-12, 41], [-17, 44], [-15, 42]]],
            ],
            {"foo": "bar"},
            {"id": "hello"},
        )

        assert len(poly.features) == 2
        assert poly.id == "hello"
        assert poly.features[0].properties["foo"] == "bar"

    def test_multi_polygon(self):

        mp = multi_polygon(
            [
                [[[94, 57], [78, 49], [94, 43], [94, 57]]],
                [[[93, 19], [63, 7], [79, 0], [93, 19]]],
            ],
            {"test": 23},
        )

        assert mp.type == "Feature"
        assert mp.properties == {"test": 23}
        assert mp.geometry.type == "MultiPolygon"
        assert mp.geometry.coordinates == [
            [[[94, 57], [78, 49], [94, 43], [94, 57]]],
            [[[93, 19], [63, 7], [79, 0], [93, 19]]],
        ]

    def test_multi_polygon_exception(self):

        with pytest.raises(Exception) as excinfo:
            multi_polygon(
                [
                    [[[0, 1], [78, 49], [94, 43], [94, 57]]],
                    [[[93, 19], [63, 7], [79, 0], [93, 19]]],
                ],
                {"test": 23},
            )
        assert "not equivalent" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            multi_polygon(
                [
                    [[[78, 49], [94, 43], [94, 57]]],
                    [[[93, 19], [63, 7], [79, 0], [93, 19]]],
                ],
                {"test": 23},
            )
        assert "4 or more Positions" in str(excinfo.value)

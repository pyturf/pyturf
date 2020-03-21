import pytest

from turf.helpers._features import point, line_string


class TestPoint:
    def test_coordinates_props(self):

        p = point([5, 10], {"name": 'test point'})

        assert p.geometry.coordinates[0] == 5
        assert p.geometry.coordinates[1] == 10
        assert p.properties["name"] == "test point"

    def test_no_props(self):

        p = point([0, 0])

        assert p.properties == {}


class TestLineString:

    def test_coordinates_props(self):

        line = line_string([[5, 10], [20, 40]], {"name": 'test line'});

        assert line.geometry.coordinates[0][0] == 5
        assert line.geometry.coordinates[1][0] == 20
        assert line.properties["name"] == "test line"

# test('lineString', t => {
#     const line = lineString([[5, 10], [20, 40]], {name: 'test line'});
# t.ok(line, 'creates a linestring');
# t.equal(line.geometry.coordinates[0][0], 5);
# t.equal(line.geometry.coordinates[1][0], 20);
# t.equal(line.properties.name, 'test line');
# t.deepEqual(lineString([[5, 10], [20, 40]]).properties, {}, 'no properties case');
#
# t.throws(() => lineString(), 'error on no coordinates');
# t.throws(() => lineString([[5, 10]]), 'coordinates must be an array of two or more positions');
# t.throws(() => lineString([['xyz', 10]]), 'coordinates must contain numbers');
# t.throws(() => lineString([[5, 'xyz']]), 'coordinates must contain numbers');
# t.end();
# });


# test('polygon', t => {
#     const poly = polygon([[[5, 10], [20, 40], [40, 0], [5, 10]]], {name: 'test polygon'});
# t.ok(poly);
# t.equal(poly.geometry.coordinates[0][0][0], 5);
# t.equal(poly.geometry.coordinates[0][1][0], 20);
# t.equal(poly.geometry.coordinates[0][2][0], 40);
# t.equal(poly.properties.name, 'test polygon');
# t.equal(poly.geometry.type, 'Polygon');
# t.throws(() => {
#     t.equal(polygon([[[20.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]).message);
# }, /First and last Position are not equivalent/, 'invalid ring - not wrapped');
# t.throws(() => {
#     t.equal(polygon([[[20.0, 0.0], [101.0, 0.0]]]).message);
# }, /Each LinearRing of a Polygon must have 4 or more Positions/, 'invalid ring - too few positions');
# const noProperties = polygon([[[5, 10], [20, 40], [40, 0], [5, 10]]]);
# t.deepEqual(noProperties.properties, {});
# t.end();
# });
#
# test('lineString', t => {
#     const line = lineString([[5, 10], [20, 40]], {name: 'test line'});
# t.ok(line, 'creates a linestring');
# t.equal(line.geometry.coordinates[0][0], 5);
# t.equal(line.geometry.coordinates[1][0], 20);
# t.equal(line.properties.name, 'test line');
# t.deepEqual(lineString([[5, 10], [20, 40]]).properties, {}, 'no properties case');
#
# t.throws(() => lineString(), 'error on no coordinates');
# t.throws(() => lineString([[5, 10]]), 'coordinates must be an array of two or more positions');
# t.throws(() => lineString([['xyz', 10]]), 'coordinates must contain numbers');
# t.throws(() => lineString([[5, 'xyz']]), 'coordinates must contain numbers');
# t.end();
# });

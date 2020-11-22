# pyturf

Read the [docs](https://pyturf.readthedocs.io/en/latest/)

![build_badge](https://github.com/pyturf/pyturf/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/pyturf/pyturf/branch/master/graph/badge.svg)](https://codecov.io/gh/pyturf/pyturf)
[![PyPI version](https://badge.fury.io/py/pyturf.svg)](https://badge.fury.io/py/pyturf)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://pyturf.readthedocs.io/?badge=latest)

`pyturf` is a powerful geospatial library written in python, based on [turf.js](https://github.com/Turfjs/turf),
a popular library written in javascript. It follows the same modular structure and maintains the same functionality as the original
modules in that library for maximum compatibility.

It includes traditional geospatial operations, as well as helper functions for creating and manipulating
[GeoJSON](https://geojson.org/) data.

## Installation

```
$ pip install pyturf
```

## Usage

Most `pyturf` modules expect as input GeoJSON features or a collection of these, which can be the following:

- Point / MultiPoint
- LineString / MultiLineString
- Polygon / MultiPolygon

These can either be defined as a python dictionary or as objects from `pyturf` helper classes.

```python
# example as a dictionary:

point1 = {
  "type": "Feature",
  "properties": {},
  "geometry": {
    "type": "Point",
    # Note order: longitude, latitude.
    "coordinates": [-73.988214, 40.749128]
  }
}

...

# Example using objects from helper classes

from turf import point

# Note order: longitude, latitude.
point1 = point([-73.988214, 40.749128])

```

In order to use the modules, one can import directly from `pyturf`, such as:

```python
from turf import distance, point

point1 = point([-73.988214, 40.749128])
point2 = point([-73.838432, 40.738484])

dist = distance(point1, point2, {"units": "miles"})
```

## Available Modules

Currently, the following modules have been implemented:

- [along](https://github.com/pyturf/pyturf/tree/master/turf/along)
- [area](https://github.com/pyturf/pyturf/tree/master/turf/area)
- [bbox](https://github.com/pyturf/pyturf/tree/master/turf/bbox)
- [bbox-polygon](https://github.com/pyturf/pyturf/tree/master/turf/bbox_polygon)
- [bearing](https://github.com/pyturf/pyturf/tree/master/turf/bearing)
- [boolean-disjoint](https://github.com/pyturf/pyturf/tree/master/turf/boolean_disjoint)
- [boolean-intersects](https://github.com/pyturf/pyturf/tree/master/turf/boolean_intersects)
- [boolean-point-in-polygon](https://github.com/pyturf/pyturf/tree/master/turf/boolean_point_in_polygon)
- [boolean-point-on-line](https://github.com/pyturf/pyturf/tree/master/turf/boolean_point_on_line)
- [boolean-within](https://github.com/pyturf/pyturf/tree/master/turf/boolean_within)
- [center](https://github.com/pyturf/pyturf/tree/master/turf/center)
- [centroid](https://github.com/pyturf/pyturf/tree/master/turf/centroid)
- [destination](https://github.com/pyturf/pyturf/tree/master/turf/destination)
- [distance](https://github.com/pyturf/pyturf/tree/master/turf/distance)
- [envelope](https://github.com/pyturf/pyturf/tree/master/turf/envelope)
- [explode](https://github.com/pyturf/pyturf/tree/master/turf/explode)
- [great circle](https://github.com/pyturf/pyturf/tree/master/turf/great_circle)
- [helpers](https://github.com/pyturf/pyturf/tree/master/turf/helpers)
- [hex_grid](https://github.com/pyturf/pyturf/tree/master/turf/hex_grid)
- [length](https://github.com/pyturf/pyturf/tree/master/turf/length)
- [line-intersect](https://github.com/pyturf/pyturf/tree/master/turf/line_intersect)
- [midpoint](https://github.com/pyturf/pyturf/tree/master/turf/midpoint)
- [nearest-point](https://github.com/pyturf/pyturf/tree/master/turf/nearest_point)
- [point-grid](https://github.com/pyturf/pyturf/tree/master/turf/point_grid)
- [point-on-feature](https://github.com/pyturf/pyturf/tree/master/turf/point_on_feature)
- [point-to-line-distance](https://github.com/pyturf/pyturf/tree/master/turf/point_to_line_distance)
- [polygon-tangents](https://github.com/pyturf/pyturf/tree/master/turf/polygon_tangents)
- [polygon-to-line](https://github.com/pyturf/pyturf/tree/master/turf/polygon_to_line)
- [rectangle-grid](https://github.com/pyturf/pyturf/tree/master/turf/rectangle_grid)
- [rhumb-bearing](https://github.com/pyturf/pyturf/tree/master/turf/rhumb_bearing)
- [rhumb-destination](https://github.com/pyturf/pyturf/tree/master/turf/rhumb_destination)
- [rhumb-distance](https://github.com/pyturf/pyturf/tree/master/turf/rhumb_distance)
- [square](https://github.com/pyturf/pyturf/tree/master/turf/square)
- [square-grid](https://github.com/pyturf/pyturf/tree/master/turf/square_grid)
- [triangle-grid](https://github.com/pyturf/pyturf/tree/master/turf/triangle_grid)

## Contributing

This library is a work in progress, so pull requests from the community are welcome!

Check out [CONTRIBUTING.md](https://github.com/pyturf/pyturf/blob/master/CONTRIBUTING.md) for a detailed explanation on how to contribute.

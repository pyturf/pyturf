# pyturf

![build_badge](https://github.com/diogomatoschaves/pyturf/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/diogomatoschaves/pyturf/branch/master/graph/badge.svg)](https://codecov.io/gh/diogomatoschaves/pyturf)

`pyturf` is a powerful geospatial library written in python, based on [turf.js](https://github.com/Turfjs/turf),
a popular library written in javascript. It follows the same modular structure and maintains the same functionality as the original
modules in that library for maximum compatibility.

It includes traditional geospatial operations, as well as helper functions for creating and manipulating
[GeoJSON](https://geojson.org/) data.

## Installation

```shell script
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

- [along](https://github.com/diogomatoschaves/pyturf/tree/master/turf/along)
- [area](https://github.com/diogomatoschaves/pyturf/tree/master/turf/area)
- [bbox](https://github.com/diogomatoschaves/pyturf/tree/master/turf/bbox)
- [bbox-polygon](https://github.com/diogomatoschaves/pyturf/tree/master/turf/bbox_polygon)
- [bearing](https://github.com/diogomatoschaves/pyturf/tree/master/turf/bearing)
- [center](https://github.com/diogomatoschaves/pyturf/tree/master/turf/center)
- [centroid](https://github.com/diogomatoschaves/pyturf/tree/master/turf/centroid)
- [destination](https://github.com/diogomatoschaves/pyturf/tree/master/turf/destination)
- [distance](https://github.com/diogomatoschaves/pyturf/tree/master/turf/distance)
- [envelope](https://github.com/diogomatoschaves/pyturf/tree/master/turf/envelope)
- [great circle](https://github.com/diogomatoschaves/pyturf/tree/master/turf/great_circle)
- [helpers](https://github.com/diogomatoschaves/pyturf/tree/master/turf/helpers)
- [length](https://github.com/diogomatoschaves/pyturf/tree/master/turf/length)
- [midpoint](https://github.com/diogomatoschaves/pyturf/tree/master/turf/midpoint)
- [rhumb-bearing](https://github.com/diogomatoschaves/pyturf/tree/master/turf/rhumb_bearing)
- [rhumb-destination](https://github.com/diogomatoschaves/pyturf/tree/master/turf/rhumb_destination)
- [rhumb-distance](https://github.com/diogomatoschaves/pyturf/tree/master/turf/rhumb_distance)
- [square](https://github.com/diogomatoschaves/pyturf/tree/master/turf/square)

## Contributing

This library is a work in progress, so pull requests from the community are welcome!

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for a detailed explanation on how to contribute.

# pyturf 

![build_badge](https://github.com/diogomatoschaves/pyturf/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/diogomatoschaves/pyturf/branch/master/graph/badge.svg)](https://codecov.io/gh/diogomatoschaves/pyturf)

`pyturf` is loosely based on [turf.js](https://github.com/Turfjs/turf), a popular geospatial engine 
written in javascript. It follows the same modular structure and maintains the same functionality as the original
modules in that library. 

It includes traditional geospatial operations, as well as helper functions for creating and manipulating 
[GeoJSON](https://geojson.org/) data. 

## Installation

`pip install pyturf`

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

## Contributing

This library is a work in progress, so pull requests from the community are welcome!

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for a detailed explanation on how to contribute.
 
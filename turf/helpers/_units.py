earth_radius = 6371008.8

factors = {
    "centimeters": earth_radius * 100,
    "centimetres": earth_radius * 100,
    "degrees": earth_radius / 111325,
    "feet": earth_radius * 3.28084,
    "inches": earth_radius * 39.370,
    "kilometers": earth_radius / 1000,
    "kilometres": earth_radius / 1000,
    "meters": earth_radius,
    "metres": earth_radius,
    "miles": earth_radius / 1609.344,
    "millimeters": earth_radius * 1000,
    "millimetres": earth_radius * 1000,
    "nautical_miles": earth_radius / 1852,
    "radians": 1,
    "yards": earth_radius / 1.0936,
}

units_factors = {
    "centimeters": 100,
    "centimetres": 100,
    "degrees": 1 / 111325,
    "feet": 3.28084,
    "inches": 39.370,
    "kilometers": 1 / 1000,
    "kilometres": 1 / 1000,
    "meters": 1,
    "metres": 1,
    "miles": 1 / 1609.344,
    "millimeters": 1000,
    "millimetres": 1000,
    "nautical_miles": 1 / 1852,
    "radians": 1 / earth_radius,
    "yards": 1 / 1.0936,
}

area_factors = {
    "acres": 0.000247105,
    "centimeters": 10000,
    "centimetres": 10000,
    "feet": 10.763910417,
    "inches": 1550.003100006,
    "kilometers": 0.000001,
    "kilometres": 0.000001,
    "meters": 1,
    "metres": 1,
    "miles": 3.86e-7,
    "millimeters": 1000000,
    "millimetres": 1000000,
    "yards": 1.195990046,
}

geometry_types = {
    "Point": "Point",
    "LineString": "LineString",
    "Polygon": "Polygon",
    "MultiPoint": "MultiPoint",
    "MultiLineString": "MultiLineString",
    "MultiPolygon": "MultiPolygon",
}

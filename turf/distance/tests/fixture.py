fixture = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]},
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [-75.534, 39.123]},
        },
    ],
}

expected_results = {
    "miles": 60.35329997171415,
    "nautical_miles": 52.44558379572265,
    "kilometers": 97.12922118967835,
    "radians": 0.015245501024842149,
    "degrees": 0.8724834600465156,
}

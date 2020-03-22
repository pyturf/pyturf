from turf.helpers import Feature, Point, LineString, MultiPoint, MultiLineString

allowed_types = ["Point", "MultiPoint", "LineString", "MultiLineString"]


def get_coord(coord):

    if isinstance(coord, list) and len(coord) == 2:
        return coord

    elif (
        isinstance(coord, Feature)
        and getattr(coord, "geometry", None)
        and getattr(coord.geometry, "type", None) in allowed_types
    ):
        return coord.geometry.coordinates

    elif isinstance(coord, (Point, MultiPoint, LineString, MultiLineString)):
        return coord.coordinates

    elif isinstance(coord, dict) and coord.get("type", None) == "Feature":
        if (
            "geometry" in coord
            and coord["geometry"].get("type", None) in allowed_types
            and "coordinates" in coord["geometry"]
        ):
            return coord["geometry"]["coordinates"]

    elif isinstance(coord, dict) and coord.get("type", None) in allowed_types:
        if "coordinates" in coord:
            return coord["coordinates"]

    raise Exception("coord must be a Point or an Array of numbers")

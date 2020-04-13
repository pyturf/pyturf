from turf.invariant import get_coord
from turf.great_circle._arc import GreatCircle


def great_circle(start, end, options=None):
    """
    Returns  the great circle route as LineString

    :param start: source point feature
    :param end: destination point feature
    :param options: Optional parameters
        [options["properties"]={}] line feature properties
        [options.npoints=100] number of points
    :return: great circle line feature
    """
    if not options or not isinstance(options, dict):
        options = {}

    start = get_coord(start)
    end = get_coord(end)

    properties = options.get("properties", {})
    npoints = options.get("npoints", 100)
    properties["npoints"] = npoints

    gc = GreatCircle(start, end, properties)

    return gc.to_geojson()

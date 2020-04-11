from turf.helpers import polygon
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


def bbox_polygon(bbox, options=None):
    """
    Takes a bounding box and returns an equivalent Polygon feature.

    :param bbox: bounding box extent in [minX, minY, maxX, maxY] order
    :param options: optional parameters
        [options["properties"]={}] Translate GeoJSON Properties to Point
        [options["id"]={}] Translate GeoJSON Id to Point
    :return: a Polygon representation of the bounding box
    """

    if not options:
        options = {}

    if not isinstance(bbox, list) or len(bbox) != 4:
        raise InvalidInput(error_code_messages["InvalidBoundingBox"])

    west = float(bbox[0])
    south = float(bbox[1])
    east = float(bbox[2])
    north = float(bbox[3])

    low_left = [west, south]
    top_left = [west, north]
    top_right = [east, north]
    low_right = [east, south]

    return polygon(
        [[low_left, low_right, top_right, top_left, low_left,]],
        options.get("properties", None),
        {"bbox": bbox, "id": options.get("id", None)},
    )

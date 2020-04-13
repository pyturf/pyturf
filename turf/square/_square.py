from turf.distance import distance

from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


def square(bbox):
    """
    Takes a bounding box and calculates the minimum square bounding box that
    would contain the input.

    :param bbox: bounding box extent in [minX, minY, maxX, maxY] order

    :return: a square surrounding bbox

    """
    if not isinstance(bbox, list) or len(bbox) != 4:
        raise InvalidInput(error_code_messages["InvalidBoundingBox"])

    west = float(bbox[0])
    south = float(bbox[1])
    east = float(bbox[2])
    north = float(bbox[3])

    horizontal_distance = distance([west, south], [east, south])
    vertical_distance = distance([west, south], [west, north])

    if horizontal_distance >= vertical_distance:
        vertical_midpoint = (south + north) / 2
        bounding_box = [
            west,
            vertical_midpoint - ((east - west) / 2),
            east,
            vertical_midpoint + ((east - west) / 2),
        ]
    else:

        horizontal_midpoint = (west + east) / 2
        bounding_box = [
            horizontal_midpoint - ((north - south) / 2),
            south,
            horizontal_midpoint + ((north - south) / 2),
            north,
        ]

    return bounding_box

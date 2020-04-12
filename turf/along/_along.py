from turf.helpers import point
from turf.bearing import bearing
from turf.destination import destination
from turf.distance import distance
from turf.invariant import get_coords_from_geometry, get_coords_from_features
from turf.utils.exceptions import InvalidInput
from turf.utils.error_codes import error_code_messages
from turf.utils.helpers import truncate


def along(line, dist, options=None):
    """
    Takes a LineString and returns a Point at a specified distance along the line

    :param line: input LineString
    :param dist: distance along the line
    :param options: optional parameters
        [options["units"]="kilometers"] can be degrees, radians, miles, or kilometers
    :return: Point `dist` `units` along the line
    """

    if not options or not isinstance(options, dict):
        options = {}

    if not isinstance(dist, (float, int)) or dist < 0:
        raise InvalidInput(error_code_messages["InvalidDistance"])

    coords = get_coords_from_features(line, ["LineString"])

    travelled = 0
    for i in range(len(coords)):
        if dist >= travelled and i == len(coords) - 1:
            break
        elif travelled >= dist:
            overshot = dist - travelled
            if not overshot:
                return point([truncate(coord, 6) for coord in coords[i]])
            else:
                direction = bearing(coords[i], coords[i - 1]) - 180
                interpolated = destination(coords[i], overshot, direction, options)
                return interpolated
        else:
            travelled += distance(coords[i], coords[i + 1])

    return point([truncate(coord, 6) for coord in coords[-1]])

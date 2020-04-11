from turf.bearing import bearing
from turf.destination import destination
from turf.distance import distance


def midpoint(point1, point2):
    """
    Takes two point features and returns a point midway between them.
    The midpoint is calculated geodesically, meaning the curvature of the earth is taken into account.

    :param point1: first point
    :param point2: second point
    :return: a point midway between point 1 and point 2
    """

    dist = distance(point1, point2)
    heading = bearing(point1, point2)
    mid_point = destination(point1, dist / 2, heading)

    return mid_point

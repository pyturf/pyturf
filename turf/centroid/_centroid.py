from functools import reduce

from turf.helpers import point
from turf.invariant import get_coords_from_features
from turf.utils.helpers import get_input_dimensions


def centroid(features, options=None):
    """
    Takes one or more features and calculates the centroid using the mean of all vertices.
    This lessens the effect of small islands and artifacts when calculating the centroid of a set of polygons.

    :param features: GeoJSON features to be centered
    :param options: optional parameters
        [options["properties"]={}] Translate GeoJSON Properties to Point
    :return: a Point feature corresponding to the centroid of the input features
    """

    if not options:
        options = {}

    coords = get_coords_from_features(features)

    if get_input_dimensions(coords) == 1:
        coords = [coords]

    x_sum = 0
    y_sum = 0
    length = 0

    x_sum, y_sum, length = reduce(reduce_coords, coords, [x_sum, y_sum, length])

    return point([x_sum / length, y_sum / length], options.get("properties", None))


def reduce_coords(sum_array, coords):

    input_dimension = get_input_dimensions(coords)

    if input_dimension >= 2:
        return reduce(lambda prev, coord: reduce_coords(prev, coord), coords, sum_array)

    return [sum_array[0] + coords[0], sum_array[1] + coords[1], sum_array[2] + 1]

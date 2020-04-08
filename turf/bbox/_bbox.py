from functools import reduce

import numpy as np

from turf.invariant import get_coords_from_features
from turf.utils.helpers import get_input_dimensions


def bbox(features):
    """
    Takes a set of features and returns a bounding box containing of all input features.

    :param features: any GeoJSON feature or feature collection
    :return: bounding box extent in [minX, minY, maxX, maxY] order
    """

    bounding_box = [np.inf, np.inf, -np.inf, -np.inf]

    coords = get_coords_from_features(features)

    if get_input_dimensions(coords) == 1:
        coords = [coords]

    return reduce(reduce_coords, coords, bounding_box)


def reduce_coords(bounding_box, coord):

    input_dimension = get_input_dimensions(coord)

    if input_dimension >= 2:
        return reduce(lambda bb, c: reduce_coords(bb, c), coord, bounding_box)

    if bounding_box[0] > coord[0]:
        bounding_box[0] = coord[0]
    if bounding_box[1] > coord[1]:
        bounding_box[1] = coord[1]
    if bounding_box[2] < coord[0]:
        bounding_box[2] = coord[0]
    if bounding_box[3] < coord[1]:
        bounding_box[3] = coord[1]

    return bounding_box

from turf.helpers import Feature, Point


def get_coord(coord):

    if isinstance(coord, list) and len(coord) == 2:
        return coord

    elif isinstance(coord, Feature) and getattr(coord, 'geometry', None) and getattr(coord.geometry, 'type', None) == 'Point':
        return coord.geometry.coordinates

    elif isinstance(coord, Point):
        return coord.coordinates

    raise Exception("coord must be a Point or an Array of numbers")

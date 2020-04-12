import numpy as np
from functools import reduce

from turf.invariant import get_geometry_from_features, get_coords_from_geometry
from turf.helpers import (
    earth_radius,
    degrees_to_radians as rad,
    get_input_dimensions,
    polygon,
)


def area(features):
    """
    Takes one or more features and returns their area in square meters.

    :param features: geojson input GeoJSON feature(s)
    :return: area in square meters
    """

    geometries = get_geometry_from_features(features)

    if not isinstance(geometries, list) or geometries == features:
        geometries = [geometries]

    return reduce(lambda prev, curr: prev + calculate_area(curr), geometries, 0)


def calculate_area(geometry):

    """
    Calculate geometry area

    :param geometry: GeoJSON geometry
    :return: the geometry area
    """

    coords = get_coords_from_geometry(
        geometry, ["Polygon", "MultiPolygon"], raise_exception=False
    )

    if get_input_dimensions(coords) >= 4:
        areas = list(map(lambda sub_item: calculate_area(sub_item), coords))
        return sum(areas)

    elif get_input_dimensions(coords) == 3:
        polygon(coords)
        return polygon_area(coords)

    else:
        return 0


def polygon_area(coords):
    """
    Calculates the area of a Polygon

    :param coords: the array of rings defining a Polygon
    :return: the total area of the Polygon
    """
    total = 0

    if len(coords) > 0:
        total += abs(ring_area(coords[0]))

    for i in coords[1:]:
        total -= abs(ring_area(coords[i]))

    return total


def ring_area(coords):
    """
    Calculate the approximate area of the polygon were it projected onto the earth.
    Note that this area will be positive if ring is oriented clockwise, otherwise it will be negative.

    Reference:
    Robert. G. Chamberlain and William H. Duquette, "Some Algorithms for Polygons on a Sphere",
    JPL Publication 07-03, Jet Propulsion
    Laboratory, Pasadena, CA, June 2007 https://trs.jpl.nasa.gov/handle/2014/40409

    :param coords: the array of coordinates defining a Polygon LinearRing
    :return: The approximate signed geodesic area of the polygon in square meters.
    """

    total = 0

    coords_length = len(coords)

    if coords_length > 2:

        for i in range(coords_length):
            if i == coords_length - 2:
                lower_index = coords_length - 2
                middle_index = coords_length - 1
                upper_index = 0

            elif i == coords_length - 1:
                lower_index = coords_length - 1
                middle_index = 0
                upper_index = 1

            else:
                lower_index = i
                middle_index = i + 1
                upper_index = i + 2

            p1 = coords[lower_index]
            p2 = coords[middle_index]
            p3 = coords[upper_index]

            total += (rad(p3[0]) - rad(p1[0])) * np.sin(rad(p2[1]))

        total = total * earth_radius ** 2 / 2

    return total

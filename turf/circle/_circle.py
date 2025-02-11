from functools import reduce
from typing import TypeVar, Dict, List

from turf import destination, polygon, Polygon
from turf.invariant import get_coords_from_features
from turf.utils.error_codes import error_code_messages
from turf.utils.exceptions import InvalidInput


Center = TypeVar("Center", List, Dict, Polygon)
Radius = TypeVar("Radius", int, float)


def add_coordinates(coords, center, radius, bearing, options):
    """
    Helper method for the reducing function. Computes a new coordinate by moving from the
    center point in a given bearing direction for a specified radius and adds it to the list of coordinates.

    :param coords: List of coordinates forming the polygon.
    :param center: Coordinates of the center point.
    :param radius: Radius of the circle.
    :param bearing: Bearing angle in degrees.
    :param options: Additional options, such as units of measurement.
    :return: Updated list of coordinates with the new computed point.
    """
    return [
        *coords,
        destination(center, radius, bearing, options=options)
        .get("geometry")
        .get("coordinates"),
    ]


def circle(center: Center, radius: Radius, options: Dict = None):
    """
    Generates a circular polygon around a given center point with a specified radius.

    :param center: The center point of the circle. Can be a list, dictionary, or Polygon.
    :param radius: The radius of the circle in specified units.
    :param options: Optional parameters
        [options["steps"] = 64] Number of steps to define the circle resolution.
        [options["properties"] = {}] Properties to include in the polygon.
    :return: A GeoJSON polygon representing the circle.
    :raises InvalidInput: If the radius is not a valid number.
    """

    if not options or not isinstance(options, dict):
        options = {}

    if "steps" not in options:
        options["steps"] = 64

    valid_center = get_coords_from_features(center, ["Point"])

    if not isinstance(radius, (float, int)):
        raise (InvalidInput(error_code_messages["InvalidRadius"]))

    properties = (
        options["properties"]
        if "properties" in options
        else (
            center["properties"]
            if (not isinstance(center, (list, tuple)) and center["type"] == "Feature")
            else {}
        )
    )

    steps = options.get("steps")

    bearings = map(lambda i: i * -360 / steps, range(steps))

    coordinates = reduce(
        lambda coords, bearing: add_coordinates(
            coords, valid_center, radius, bearing, options
        ),
        bearings,
        [],
    )

    coordinates.append(coordinates[0])

    return polygon([coordinates], properties)

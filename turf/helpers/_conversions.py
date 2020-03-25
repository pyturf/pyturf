import numpy as np

from turf.helpers._units import factors, area_factors
from turf.utils.exceptions import InvalidInput
from turf.utils.error_codes import error_code_messages


def c_like_modulo(number, base):

    return number - int(number / base) * base


def degrees_to_radians(degrees):
    """
    :param degrees: degrees angle
    :return: angle in radians
    """

    if not isinstance(degrees, (float, int)):
        raise InvalidInput(error_code_messages["InvalidDegrees"])

    radians = c_like_modulo(degrees, 360)
    return radians * np.pi / 180


def radians_to_degrees(radians):
    """
    :param radians: radians angle in radians
    :return: degrees between 0 and 360
    """

    if not isinstance(radians, (float, int)):
        raise InvalidInput(error_code_messages["InvalidRadians"])

    degrees = c_like_modulo(radians, 2 * np.pi)
    return degrees * 180 / np.pi


def length_to_radians(distance, units="kilometers"):
    """
    :param distance: distance in real units
    :param units: units of the distance. Can be degrees, radians, miles, kilometers,
            inches, yards, metres, meters, kilometres, kilometers. Defaults to kilometers
    :return: radians
    """

    if not isinstance(distance, (float, int)):
        raise (InvalidInput(error_code_messages["InvalidDistance"]))

    try:
        factor = factors[units]
    except KeyError:
        raise InvalidInput(error_code_messages["InvalidUnits"](units))

    return distance / factor


def radians_to_length(radians, units="kilometers"):
    """
    :param radians: radians in radians across the sphere
    :param units: units of the distance. Can be degrees, radians, miles, kilometers,
            inches, yards, metres, meters, kilometres, kilometers. Defaults to kilometers
    :return: distance
    """

    try:
        factor = factors[units]
    except KeyError:
        raise InvalidInput(error_code_messages["InvalidUnits"](units))

    return radians * factor


def length_to_degrees(distance, units="kilometers"):
    """
    :param distance: distance in real units
    :param units: units of the distance. Can be degrees, radians, miles, kilometers,
            inches, yards, metres, meters, kilometres, kilometers. Defaults to kilometers
    :return: degrees
    """

    return radians_to_degrees(length_to_radians(distance, units))


def convert_length(length, original_unit="kilometers", final_unit="kilometers"):
    """
    :param length: length to be converted
    :param original_unit: original unit of the length
    :param final_unit: return unit of the length
    :return: the converted length
    """

    if not isinstance(length, (float, int)) or length < 0:
        raise InvalidInput(error_code_messages["InvalidLength"])

    return radians_to_length(length_to_radians(length, original_unit), final_unit)


def convert_area(area, original_unit="meters", final_unit="kilometers"):
    """
    :param area: area to be converted
    :param original_unit: original unit of the area
    :param final_unit: returned unit of area
    :return: the converted area
    """

    if not isinstance(area, (float, int)) or area < 0:
        raise InvalidInput(error_code_messages["InvalidArea"])

    try:
        start_factor = area_factors[original_unit]
    except KeyError:
        raise InvalidInput(
            InvalidInput(error_code_messages["InvalidUnits"](original_unit))
        )

    try:
        final_factor = area_factors[final_unit]
    except KeyError:
        raise InvalidInput(
            InvalidInput(error_code_messages["InvalidUnits"](final_unit))
        )

    return (area / start_factor) * final_factor

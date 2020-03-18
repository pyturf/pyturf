import numpy as np

from turf.helpers._units import factors, area_factors


def c_like_modulo(number, base):

    return number - int(number / base) * base


def degrees_to_radians(degrees):
    """
    :param degrees: degrees angle
    :return: angle in radians
    """

    radians = c_like_modulo(degrees, 360)
    return radians * np.pi / 180


def radians_to_degrees(radians):
    """
    :param radians: radians angle in radians
    :return: degrees between 0 and 360
    """

    degrees = c_like_modulo(radians, 2 * np.pi)
    return degrees * 180 / np.pi


def length_to_radians(distance, units="kilometers"):
    """
    :param distance: distance in real units
    :param units: units of the distance. Can be degrees, radians, miles, kilometers,
            inches, yards, metres, meters, kilometres, kilometers. Defaults to kilometers
    :return: radians
    """

    try:
        factor = factors[units]
    except KeyError:
        raise Exception(f"{units} is not a valid unit")

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
        raise Exception(f"{units} is not a valid unit")

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

    if not length >= 0:
        raise Exception("length must be a positive number")

    return radians_to_length(length_to_radians(length, original_unit), final_unit)


def convert_area(area, original_unit="meters", final_unit="kilometers"):
    """
    :param area: area to be converted
    :param original_unit: original unit of the area
    :param final_unit: returned unit of area
    :return: the converted area
    """

    if not area >= 0:
        raise Exception("area must be a positive number")

    try:
        start_factor = area_factors[original_unit]
    except KeyError:
        raise Exception(f"{original_unit} is not a valid unit")

    try:
        final_factor = area_factors[final_unit]
    except KeyError:
        raise Exception(f"{final_unit} is not a valid unit")

    return (area / start_factor) * final_factor

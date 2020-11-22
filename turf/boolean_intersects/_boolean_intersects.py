from typing import Any

from turf.boolean_disjoint import boolean_disjoint


def boolean_intersects(feature_1: Any, feature_2: Any) -> bool:
    """
    Returns true if the two geometries intersect.

    :param feature_1: {GeoJSON} feature_1 any Feature or Geometry
    :param feature_2: {GeoJSON} feature_2 any Feature or Geometry
    :return: boolean True/False if features intersect
    """
    return not boolean_disjoint(feature_1, feature_2)

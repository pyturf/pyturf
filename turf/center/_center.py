from turf.helpers import point
from turf.bbox import bbox


def center(features, options=None):
    """
    Takes a Feature or FeatureCollection and returns the absolute center point of all features.

    :param features: features or collection of features
    :param options: optional parameters
        [options["properties"]={}] Translate GeoJSON Properties to Point
        [options["bbox"]={}] Translate GeoJSON BBox to Point
        [options["id"]={}] Translate GeoJSON Id to Point
    :return: a Point feature at the absolute center point of all input features
    """

    if not options or not isinstance(options, dict):
        options = {}

    bounding_box = bbox(features)
    x = (bounding_box[0] + bounding_box[2]) / 2
    y = (bounding_box[1] + bounding_box[3]) / 2

    return point([x, y], options.get("properties", {}), options)

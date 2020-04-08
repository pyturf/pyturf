from turf.bbox import bbox
from turf.bbox_polygon import bbox_polygon


def envelope(features, *args):
    """
    Takes any number of features and returns a rectangular Polygon that encompasses all vertices.

    :param features: any GeoJSON feature or feature collection
    :return: bounding box extent in [minX, minY, maxX, maxY] order
    """
<<<<<<< HEAD
    return bbox_polygon(bbox(geojson, *args))
=======

    return bbox_polygon(bbox(features, *args))
>>>>>>> added tests

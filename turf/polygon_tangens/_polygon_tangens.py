from typing import Dict, List, Sequence, TypeVar

from turf.bbox import bbox
from turf.helpers import FeatureCollection, MultiPolygon, Point, Polygon
from turf.invariant import get_coords_from_features

PointFeature = TypeVar("PointFeature", Dict, Point, Sequence)
PolygonFeature = TypeVar("PolygonFeature", Dict, Polygon, MultiPolygon)


def polygon_tangens(point: PointFeature, polygon: PolygonFeature) -> FeatureCollection:
    """ Finds the tangents of a {Polygon|(Multi)Polygon} from a {Point}.

    :param point: point [lng, lat] or Point feature to calculate the tangent points from
    :param polygon: polygon to get tangents from

    :return:
        Feature Collection containing the two tangent points
    """

    point_coords = get_coords_from_features(point, ["Point"])
    polygon_coords = get_coords_from_features(polygon, ["Polygon"])

    bbox = bbox(polygon)

    nearest_pt_index = 0
    nearest = None

    # If the point lies inside the polygon bbox then we need to be a bit trickier
    # otherwise points lying inside reflex angles on concave polys can have issues
    if (point_coords[0] > bbox[0]) and (point_coords[0] < bbox[2]) and \
       (point_coords[1] > bbox[1]) and (point_coords[1] < bbox[3]):
        nearest = nearest_point(point, explode(polygon))
        nearest_pt_index = nearest["properties"]["featureIndex"]

    if type(polygon) == "Polygon":
        rtan = poly_coords[0][nearest_pt_index]
        ltan = poly_coords[0][0]
        if nearest:
            if nearest["geometry"]["coordinates"][1] < point_coords[1]:
                ltan = poly_coords[0][nearest_pt_index]

        eprev = is_left(poly_coords[0][0], poly_coords[0][len(poly_coords[0]) - 1], point_coords)
        out = process_polygon(poly_coords[0], point_coords, eprev, enext, rtan, ltan, polygon)
        rtan = out[0]
        ltan = out[1]
        break

    elif type(polygon) == "MultiPolygon":

        closest_feature = 0
        closest_vertex = 0
        vertices_counted = 0

        for i in range(len(polygon_coords)):

            closest_feature = i
            vertice_found = False
            for i2 in range(len(polygon_coords[0][i])):
                closest_vertex = i2
                if (vertices_counted == nearest_pt_index):
                    vertice_found = True
                    break

                vertices_counted += 1

            if vertice_found:
                break

        rtan = polygon_coords[0][closest_feature][closest_vertex]
        ltan = polygon_coords[0][closest_feature][closest_vertex]
        eprev = is_left(polygon_coords[0][0][0],
                        polygon_coords[0][0][len(polygon_coords[0][0]) - 1],
                        point_coords)

        for ring in poly_coords:
            out = processPolygon(ring[0], point_coords, eprev, enext, rtan, ltan, polygon);
            rtan = out[0]
            ltan = out[1]

    return feature_collection([point(rtan), point(ltan)])


def process_polygon(poly_coords, pt_coords, eprev, enext, rtan, ltan):
    for i in range(1,len(poly_coords)):

        current_poly_coord = poly_coords[i-1]

        if i == len(poly_coords):
            next_poly_coord = poly_coords[0]
        else:
            next_poly_coord = poly_coords[i]

        enext = is_left(current_poly_coord, next_poly_coord, pt_coords)

        if (eprev <= 0) and (enext > 0):

            if not is_below(pt_coords, current_poly_coord, rtan):
                rtan = current_poly_coord

        elif (eprev > 0) and (enext <= 0):
            if not is_above(pt_coords, current_poly_coord, ltan):
                ltan = current_poly_coord

        eprev = enext

    return [rtan, ltan]


def is_above(point1, point2, point3):
    return is_left(point1, point2, point3) > 0
}

def is_below(point1, point2, point3):
    return is_left(point1, point2, point3) < 0
}

def is_left(point1, point2, point3):
    return (point2[0] - point1[0]) * (point3[1] - point1[1]) - \
           (point3[0] - point1[0]) * (point2[1] - point1[1])

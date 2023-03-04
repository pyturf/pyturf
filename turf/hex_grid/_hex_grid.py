from typing import Dict, List, Union
import math

from turf.distance import distance
from turf.bbox import bbox
from turf.boolean_intersects import boolean_intersects
from turf.helpers import feature_collection, polygon, FeatureCollection


def hex_grid(
    bbox: List[float],
    cell_side: Union[int, float],
    options: Dict = {},
) -> FeatureCollection:
    """
    Takes a bounding box and the diameter of the cell and returns a FeatureCollection of flat-topped
    hexagons or triangles aligned in an "odd-q" vertical grid as
    described in [Hexagonal Grids](http://www.redblobgames.com/grids/hexagons/).

    :param bbox: Array extent in [minX, minY, maxX, maxY] order
    :param n_cells: length of the side of the the hexagons or triangles, in units. It will also coincide with the
                    radius of the circumcircle of the hexagons
    :param options: Optional parameters
        [options["units"]]: units ("degrees", "radians", "miles", "kilometers")
                            of the given cell_width and cell_height
        [options["mask"]]: if passed a Polygon or MultiPolygon here,
                           the grid Points will be created only inside it
        [options["properties"]]: passed to each point of the grid
        [options["triangles"]]: whether to return as triangles instead of hexagons

    :returns: FeatureCollection of a grid of polygons
    """
    if not isinstance(options, dict):
        options = {}

    has_triangles = options.get("triangles", None)

    results = []
    west = bbox[0]
    south = bbox[1]
    east = bbox[2]
    north = bbox[3]

    center_y = (south + north) / 2
    center_x = (west + east) / 2

    x_fraction = (cell_side * 2) / (
        distance([west, center_y], [east, center_y], options)
    )
    cell_width_deg = x_fraction * (east - west)
    y_fraction = (
        cell_side * 2 / (distance([center_x, south], [center_x, north], options))
    )
    cell_height_deg = y_fraction * (north - south)
    radius = cell_width_deg / 2

    hex_width = radius * 2
    hex_height = math.sqrt(3) / 2 * cell_height_deg

    # rows & columns
    bbox_width = east - west
    bbox_height = north - south

    x_interval = 3 / 4 * hex_width
    y_interval = hex_height

    x_span = (bbox_width - hex_width) / (hex_width - radius / 2)
    x_count = int(x_span)

    x_adjust = (
        ((x_count * x_interval - radius / 2) - bbox_width) / 2
        - radius / 2
        + x_interval / 2
    )

    y_count = int((bbox_height - hex_height) / hex_height)
    y_adjust = (bbox_height - y_count * hex_height) / 2

    has_offset_y = (y_count * hex_height - bbox_height) > (hex_height / 2)

    if has_offset_y:
        y_adjust -= hex_height / 4

    cosines = []
    sines = []

    for i in range(6):
        angle = 2 * math.pi / 6 * i
        cosines.append(math.cos(angle))
        sines.append(math.sin(angle))

    results = []

    for x in range(x_count + 1):
        for y in range(y_count + 1):
            is_odd = x % 2 == 1

            if (y == 0) and is_odd:
                continue

            if (y == 0) and has_offset_y:
                continue

            center_x = x * x_interval + west - x_adjust
            center_y = y * y_interval + south + y_adjust

            if is_odd:
                center_y -= hex_height / 2

            if has_triangles:
                triangles = hex_triangles(
                    [center_x, center_y],
                    cell_width_deg / 2,
                    cell_height_deg / 2,
                    options.get("properties", {}).copy(),
                    cosines,
                    sines,
                )

                for triangle in triangles:
                    if "mask" in options:
                        if boolean_intersects(options["mask"], triangle):
                            results.append(triangle)
                    else:
                        results.append(triangle)

            else:
                hex = hexagon(
                    [center_x, center_y],
                    cell_width_deg / 2,
                    cell_height_deg / 2,
                    options.get("properties", {}).copy(),
                    cosines,
                    sines,
                )

                if "mask" in options:
                    if boolean_intersects(options["mask"], hex):
                        results.append(hex)
                else:
                    results.append(hex)

    return feature_collection(results)


def hexagon(center, rx, ry, properties, cosines, sines):
    vertices = []
    for i in range(6):
        x = center[0] + rx * cosines[i]
        y = center[1] + ry * sines[i]
        vertices.append([x, y])

    vertices.append(vertices[0])
    return polygon([vertices], properties)


def hex_triangles(center, rx, ry, properties, cosines, sines):
    triangles = []
    for i in range(6):
        vertices = []
        vertices.append(center)
        vertices.append([center[0] + rx * cosines[i], center[1] + ry * sines[i]])
        vertices.append(
            [center[0] + rx * cosines[(i + 1) % 6], center[1] + ry * sines[(i + 1) % 6]]
        )
        vertices.append(center)
        triangles.append(polygon([vertices], properties))

    return triangles

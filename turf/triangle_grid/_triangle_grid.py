from typing import Dict, List, Union

from turf.distance import distance
from turf.bbox import bbox
from turf.boolean_intersects import boolean_intersects
from turf.helpers import feature_collection, polygon, FeatureCollection


def triangle_grid(
    bbox: List[float],
    cell_side: Union[int, float],
    options: Dict = {},
) -> FeatureCollection:
    """
    Creates a square of rectangles from a bounding box, Feature or FeatureCollection.

    :param bbox: Array extent in [minX, minY, maxX, maxY] order
    :param cell_side: dimension of each cell
    :param options: Optional parameters
        [options["units"]]: units ("degrees", "radians", "miles", "kilometers")
                            of the given cell_width and cell_height
        [options["mask"]]: if passed a Polygon or MultiPolygon here,
                           the grid Points will be created only inside it
        [options["properties"]]: passed to each point of the grid

    :returns: FeatureCollection of a grid of polygons
    """
    if not isinstance(options, dict):
        options = {}

    results = []
    west = bbox[0]
    south = bbox[1]
    east = bbox[2]
    north = bbox[3]

    x_fraction = cell_side / (distance([west, south], [east, south], options))
    cell_width_deg = x_fraction * (east - west)
    y_fraction = cell_side / (distance([west, south], [west, north], options))
    cell_height_deg = y_fraction * (north - south)

    # if the grid does not fill the bbox perfectly, center it.
    xi = 0
    current_x = west
    while current_x <= east:
        yi = 0
        current_y = south
        while current_y <= north:
            cell_triangle1 = None
            cell_triangle2 = None

            if (xi % 2 == 0) and (yi % 2 == 0):
                cell_triangle1 = polygon(
                    [
                        [
                            [current_x, current_y],
                            [current_x, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y],
                            [current_x, current_y],
                        ]
                    ],
                    options.get("properties", {}),
                )

                cell_triangle2 = polygon(
                    [
                        [
                            [current_x, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y],
                            [current_x, current_y + cell_height_deg],
                        ]
                    ],
                    options.get("properties", {}),
                )

            elif (xi % 2 == 0) and (yi % 2 == 1):
                cell_triangle1 = polygon(
                    [
                        [
                            [current_x, current_y],
                            [current_x + cell_width_deg, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y],
                            [current_x, current_y],
                        ]
                    ],
                    options.get("properties", {}),
                )

                cell_triangle2 = polygon(
                    [
                        [
                            [current_x, current_y],
                            [current_x, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y + cell_height_deg],
                            [current_x, current_y],
                        ]
                    ],
                    options.get("properties", {}),
                )

            elif (yi % 2 == 0) and (xi % 2 == 1):
                cell_triangle1 = polygon(
                    [
                        [
                            [current_x, current_y],
                            [current_x, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y + cell_height_deg],
                            [current_x, current_y],
                        ]
                    ],
                    options.get("properties", {}),
                )

                cell_triangle2 = polygon(
                    [
                        [
                            [current_x, current_y],
                            [current_x + cell_width_deg, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y],
                            [current_x, current_y],
                        ]
                    ],
                    options.get("properties", {}),
                )

            elif (yi % 2 == 1) and (xi % 2 == 1):
                cell_triangle1 = polygon(
                    [
                        [
                            [current_x, current_y],
                            [current_x, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y],
                            [current_x, current_y],
                        ]
                    ],
                    options.get("properties", {}),
                )

                cell_triangle2 = polygon(
                    [
                        [
                            [current_x, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y + cell_height_deg],
                            [current_x + cell_width_deg, current_y],
                            [current_x, current_y + cell_height_deg],
                        ]
                    ],
                    options.get("properties", {}),
                )

            if "mask" in options:
                if boolean_intersects(options["mask"], cell_triangle1):
                    results.append(cell_triangle1)
                if boolean_intersects(options["mask"], cell_triangle2):
                    results.append(cell_triangle2)
            else:
                results.append(cell_triangle1)
                results.append(cell_triangle2)

            current_y += cell_height_deg
            yi += 1

        current_x += cell_width_deg
        xi += 1

    return feature_collection(results)

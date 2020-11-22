from typing import Dict, List, Union

from turf.distance import distance
from turf.bbox import bbox
from turf.boolean_intersects import boolean_intersects
from turf.helpers import feature_collection, polygon, FeatureCollection


def rectangle_grid(
    bbox: List[float],
    cell_width: Union[int, float],
    cell_height: Union[int, float],
    options: Dict = {},
) -> FeatureCollection:
    """
    Creates a grid of rectangles from a bounding box, Feature or FeatureCollection.

    :param bbox: Array extent in [minX, minY, maxX, maxY] order
    :param cell_width: of each cell, in units
    :param cell_height: of each cell, in units

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

    x_fraction = cell_width / (distance([west, south], [east, south], options))
    cell_width_deg = x_fraction * (east - west)
    y_fraction = cell_height / (distance([west, south], [west, north], options))
    cell_height_deg = y_fraction * (north - south)

    # rows & columns
    bbox_width = east - west
    bbox_height = north - south
    columns = int(bbox_width // cell_width_deg)
    rows = int(bbox_height // cell_height_deg)

    # if the grid does not fill the bbox perfectly, center it.
    delta_x = (bbox_width - columns * cell_width_deg) / 2
    delta_y = (bbox_height - rows * cell_height_deg) / 2

    # iterate over columns & rows
    current_x = west + delta_x
    for _ in range(columns):
        current_y = south + delta_y
        for _ in range(rows):
            cell_poly = polygon(
                [
                    [
                        [current_x, current_y],
                        [current_x, current_y + cell_height_deg],
                        [current_x + cell_width_deg, current_y + cell_height_deg],
                        [current_x + cell_width_deg, current_y],
                        [current_x, current_y],
                    ]
                ],
                options.get("properties", {}),
            )

            if "mask" in options:
                if boolean_intersects(options["mask"], cell_poly):
                    results.append(cell_poly)
            else:
                results.append(cell_poly)

            current_y += cell_height_deg

        current_x += cell_width_deg

    return feature_collection(results)

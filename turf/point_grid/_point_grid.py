from typing import Dict, List, Union

from turf.distance import distance
from turf.bbox import bbox
from turf.boolean_within import boolean_within
from turf.helpers import feature_collection, point, FeatureCollection


def point_grid(
    bbox: List[float],
    n_cells: Union[int, float],
    options: Dict = {},
) -> FeatureCollection:
    """
    Creates a square of rectangles from a bounding box, Feature or FeatureCollection.

    :param bbox: Array extent in [minX, minY, maxX, maxY] order
    :param n_cells: number of each cell, in units
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

    x_fraction = n_cells / (distance([west, south], [east, south], options))
    cell_width_deg = x_fraction * (east - west)
    y_fraction = n_cells / (distance([west, south], [west, north], options))
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
    while current_x <= east:
        current_y = south + delta_y
        while current_y <= north:
            cell_point = point([current_x, current_y], options.get("properties", {}))

            if "mask" in options:
                if boolean_within(cell_point, options["mask"]):
                    results.append(cell_point)
            else:
                results.append(cell_point)

            current_y += cell_height_deg

        current_x += cell_width_deg

    return feature_collection(results)

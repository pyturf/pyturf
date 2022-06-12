from typing import Dict, List, Union

from turf.helpers import FeatureCollection
from turf.rectangle_grid import rectangle_grid


def square_grid(
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

    return rectangle_grid(bbox, n_cells, n_cells, options)

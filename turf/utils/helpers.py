def get_input_dimensions(lst, n_dim=0):
    if isinstance(lst, list):
        return get_input_dimensions(lst[0], n_dim + 1) if len(lst) > 0 else 0
    else:
        return n_dim


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


dimensions = {
    "Point": 1,
    "MultiPoint": 2,
    "LineString": 2,
    "MultiLineString": 3,
    "Polygon": 3,
    "MultiPolygon": 4,
}

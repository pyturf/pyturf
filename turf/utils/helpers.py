def get_input_dimensions(lst, n_dim=0):
    if isinstance(lst, list):
        return get_input_dimensions(lst[0], n_dim + 1)
    else:
        return n_dim

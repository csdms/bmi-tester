import numpy as np


def test_grid_x(initialized_bmi, gid):
    gtype = initialized_bmi.get_grid_type(gid)
    if gtype == "unstructured":
        ndim = bmi.get_grid_rank(gid)
        size = bmi.get_grid_size(gid)

        x = np.full(size, np.nan)
        assert x is bmi.get_grid_x(gid, x)
        assert np.all(~np.isnan(arr))

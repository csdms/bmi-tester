import warnings

import numpy as np


def test_get_grid_shape(initialized_bmi, gid):
    """Test the grid shape."""
    gtype = initialized_bmi.get_grid_type(gid)
    if gtype == "uniform_rectilinear":
        ndim = initialized_bmi.get_grid_rank(gid)

        shape = np.empty(ndim, dtype=np.int32)
        try:
            rtn = initialized_bmi.get_grid_shape(gid, shape)
        except TypeError:
            warnings.warn("get_grid_shape should take two arguments")
            rtn = initialized_bmi.get_grid_shape(gid)
            shape[:] = rtn
        else:
            assert rtn is shape

        for dim in shape:
            assert dim > 0


def test_get_grid_spacing(initialized_bmi, gid):
    """Test the grid spacing."""
    gtype = initialized_bmi.get_grid_type(gid)
    if gtype == "uniform_rectilinear":
        ndim = initialized_bmi.get_grid_rank(gid)

        spacing = np.empty(ndim, dtype=float)
        assert spacing is initialized_bmi.get_grid_spacing(gid, spacing)

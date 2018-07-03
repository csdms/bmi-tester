import warnings

import numpy as np


def test_get_grid_shape(new_bmi, gid):
    """Test the grid shape."""
    gtype = new_bmi.get_grid_type(gid)
    if gtype == 'uniform_rectilinear':
        ndim = new_bmi.get_grid_rank(gid)

        shape = np.empty(ndim, dtype=np.int32)
        try:
            rtn = new_bmi.get_grid_shape(gid, shape)
        except TypeError:
            warnings.warn('get_grid_shape should take two arguments')
            rtn = new_bmi.get_grid_shape(gid)
            shape[:] = rtn
        else:
            assert rtn is shape

        for dim in shape:
            assert dim > 0

    if gtype == 'scalar':
        ndim = new_bmi.get_grid_rank(gid)

        shape = np.empty(ndim, dtype=np.int32)
        try:
            rtn = new_bmi.get_grid_shape(gid, shape)
        except TypeError:
            warnings.warn('get_grid_shape should take two arguments')
            rtn = new_bmi.get_grid_shape(gid)
        else:
            assert rtn is shape
        np.testing.assert_equal(shape, ())


def test_get_grid_spacing(new_bmi, gid):
    """Test the grid spacing."""
    gtype = new_bmi.get_grid_type(gid)
    if gtype == 'uniform_rectilinear':
        ndim = new_bmi.get_grid_rank(gid)

        spacing = np.empty(ndim, dtype=float)
        assert spacing is new_bmi.get_grid_spacing(gid, spacing)
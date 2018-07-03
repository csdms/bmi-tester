import numpy as np
from nose.tools import assert_is_instance, assert_equal
from nose import with_setup

from .utils import setup_func, teardown_func, all_grids, new_bmi


@with_setup(setup_func, teardown_func)
def test_get_grid_shape():
    """Test the grid shape."""
    """Note: the shape of the grid determines which BMI functions are
    used to access the grid's properties"""
    bmi = new_bmi()
    for gid in all_grids(bmi, gtype="uniform_rectilinear"):

        def _check_shape(bmi, gid):
            shape = bmi.get_grid_shape(gid)
            assert_is_instance(shape, tuple)
            ndim = len(shape)
            assert_equal(ndim, bmi.get_grid_rank(gid))
            for dim in shape:
                assert_is_instance(dim, int)

        _check_shape.description = "Test grid shape for uniform rectilinear grid {gid}".format(
            gid=gid
        )
        yield _check_shape, bmi, gid

    for gid in all_grids(bmi, gtype="scalar"):

        def _check_shape(bmi, gid):
            shape = bmi.get_grid_shape(gid)
            assert_is_instance(shape, tuple)
            np.testing.assert_equal(shape, ())

        _check_shape.description = "Test grid shape for scalar grid {gid}".format(
            gid=gid
        )
        yield _check_shape, bmi, gid


@with_setup(setup_func, teardown_func)
def test_get_grid_spacing():
    """Test the grid spacing."""
    bmi = new_bmi()
    for gid in all_grids(bmi, gtype="uniform_rectilinear"):

        def _check_spacing(bmi, gid):
            spacing = bmi.get_grid_spacing(gid)
            assert_is_instance(spacing, tuple)
            ndim = len(spacing)
            assert_equal(ndim, bmi.get_grid_rank(gid))
            for dim in spacing:
                assert_is_instance(dim, (int, float))

        _check_spacing.description = "Test grid spacing for uniform rectilinear grid {gid}".format(
            gid=gid
        )
        yield _check_spacing, bmi, gid

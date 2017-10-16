from nose.tools import (assert_is_instance, assert_less_equal, assert_equal,
                        assert_greater, assert_in)
from nose import with_setup

from .utils import setup_func, teardown_func, all_names, all_grids, new_bmi


@with_setup(setup_func, teardown_func)
def test_get_grid_rank():
    """Test the rank of the grids."""
    bmi = new_bmi()
    for gid in all_grids(bmi):
        def _check_rank(bmi, gid):
            rank = bmi.get_grid_rank(gid)
            assert_is_instance(rank, int)
            assert_less_equal(rank, 3)
        _check_rank.description = 'Test rank of {gid}'.format(gid=gid)

        yield _check_rank, bmi, gid


@with_setup(setup_func, teardown_func)
def test_get_grid_size():
    bmi = new_bmi()
    for gid in all_grids(bmi):
        def _check_grid_size(bmi, gid):
            size = bmi.get_grid_size(gid)
            assert_is_instance(size, int)
            assert_greater(size, 0)
        _check_grid_size.description = "Test grid size for grid {gid}".format(gid=gid)
        yield _check_grid_size, bmi, gid


@with_setup(setup_func, teardown_func)
def test_get_grid_type():
    """Test the grid type."""
    bmi = new_bmi()
    for gid in all_grids(bmi):
        def _check_type_is_valid(gtype):
            assert_in(gtype, ("scalar", "unstructured", "rectilinear",
                              "structured_quadrilateral",
                              "uniform_rectilinear"))
        _check_type_is_valid.description = "Test grid is known for grid {gid}".format(gid=gid)

        def _check_type_is_str(gtype):
            assert_is_instance(gtype, str)
        _check_type_is_str.description = "Test grid type is str for grid {gid}".format(gid=gid)

        yield _check_type_is_valid, bmi.get_grid_type(gid)
        yield _check_type_is_str, bmi.get_grid_type(gid)

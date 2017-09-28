from nose.tools import assert_is_instance, assert_equal
from nose import with_setup

from .utils import setup_func, teardown_func, all_grids, new_bmi


@with_setup(setup_func, teardown_func)
def test_grid_x():
    bmi = new_bmi()
    for gid in all_grids(bmi, gtype='unstructured'):
        def _check_array_is_ndarray(arr):
            assert_is_instance(arr, np.ndarray)
        _check_array_is_ndarray.description = "Test x for grid {gid} is ndarray".format(gid=gid)
        def _check_array_length(arr, size):
            assert_equal(len(arr), size)
        _check_array_length.description = "Test length of x for grid {gid}".format(gid=gid)
        def _check_array_type(arr):
            assert_equal(arr.dtype, np.dtype(float))
        _check_array_length.description = "Test x for grid {gid} is float".format(gid=gid)

        yield _check_array_is_ndarray, bmi.get_grid_x(gid)
        yield _check_array_length, bmi.get_grid_x(gid), bmi.get_grid_size(gid)
        yield _check_array_type, bmi.get_grid_x(gid)

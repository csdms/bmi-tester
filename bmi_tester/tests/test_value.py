from __future__ import print_function
import warnings

import numpy as np
from nose.tools import assert_is_instance, assert_equal
from nose import with_setup

from .utils import setup_func, teardown_func, all_names, new_bmi


@with_setup(setup_func, teardown_func)
def test_get_input_values():
    """Input values are numpy arrays."""
    bmi = new_bmi()
    names = bmi.get_input_var_names()
    for name in names:
        gid = bmi.get_var_grid(name)
        if hasattr(bmi, 'get_var_location'):
            loc = bmi.get_var_location(name)
        else:
            warnings.warn('get_var_location not implemented (assuming nodes)', FutureWarning)
            loc = 'node'
        if loc == 'node':
            size = bmi.get_grid_size(gid)
        elif loc == 'edge':
            size = bmi.get_grid_number_of_edges(gid)

        def _check_is_ndarray(arr):
            assert_is_instance(arr, np.ndarray)
        _check_is_ndarray.description = 'Test input {name} is ndarray'.format(name=name)
        def _check_array_length(arr, _size):
            assert_equal(len(arr), _size)
        _check_array_length.description = 'Test input {name} is length {size}'.format(name=name, size=size)

        yield _check_is_ndarray, bmi.get_value(name)
        yield _check_array_length, bmi.get_value(name), size


@with_setup(setup_func, teardown_func)
def test_get_output_values():
    """Output values are numpy arrays."""
    bmi = new_bmi()
    names = bmi.get_output_var_names()
    for name in names:
        gid = bmi.get_var_grid(name)
        if hasattr(bmi, 'get_var_location'):
            loc = bmi.get_var_location(name)
        else:
            warnings.warn('get_var_location not implemented (assuming nodes)', FutureWarning)
            loc = 'node'
        if loc == 'node':
            size = bmi.get_grid_size(gid)
        elif loc == 'edge':
            size = bmi.get_grid_number_of_edges(gid)
        def _check_is_ndarray(arr):
            assert_is_instance(arr, np.ndarray)
        _check_is_ndarray.description = 'Test output {name} is ndarray'.format(name=name)
        def _check_array_length(arr, _size):
            assert_equal(len(arr), _size)
        _check_array_length.description = 'Test output {name} is length {size}'.format(name=name, size=size)

        yield _check_is_ndarray, bmi.get_value(name)
        yield _check_array_length, bmi.get_value(name), size


@with_setup(setup_func, teardown_func)
def test_get_value_ref():
    """Test if can get reference for value"""
    bmi = new_bmi()
    for name in all_names(bmi):
        def _check_array_is_equal(arr1, arr2):
            np.array_equal(arr1, np.asarray(arr2))
        _check_array_is_equal.description = 'Test array reference for {name}'.format(name=name)
        yield _check_array_is_equal, bmi.get_value(name), bmi.get_value_ref(name)

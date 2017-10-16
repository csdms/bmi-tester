import numpy as np
from nose.tools import assert_is_instance, assert_equal
from nose import with_setup

import cfunits

from .utils import setup_func, teardown_func, all_grids, all_names, new_bmi


@with_setup(setup_func, teardown_func)
def test_get_var_grid():
    """Test the grid of the variables."""
    bmi = new_bmi()
    for name in all_names(bmi):
        gid = bmi.get_var_grid(name)
        def _check_var_grid_is_int(_gid):
            assert_is_instance(_gid, int)
        _check_var_grid_is_int.description = 'Test grid id is int'

        yield _check_var_grid_is_int, gid


@with_setup(setup_func, teardown_func)
def test_get_var_itemsize():
    """Test getting a variable's itemsize"""
    bmi = new_bmi()
    for name in all_names(bmi):
        def _check_var_itemsize(bmi, _name):
            val = bmi.get_value(_name)
            np.testing.assert_equal(val.itemsize, bmi.get_var_itemsize(_name))

        _check_var_itemsize.description = "Test get_var_itemsize for {name}".format(name=name)

        yield _check_var_itemsize, bmi, name


@with_setup(setup_func, teardown_func)
def test_get_var_nbytes():
    """Test getting a variable's nbytes"""
    bmi = new_bmi()
    for name in all_names(bmi):
        def _check_var_nbytes(bmi, _name):
            val = bmi.get_value(_name)
            val_nbytes = val.nbytes
            np.testing.assert_equal(val_nbytes, bmi.get_var_nbytes(_name))

        _check_var_nbytes.description = "Test get_val_nbytes for {name}".format(name=name)

        yield _check_var_nbytes, bmi, name


@with_setup(setup_func, teardown_func)
def test_get_var_type():
    """Test getting a variable's data type"""
    bmi = new_bmi()
    for name in all_names(bmi):
        def _check_var_type(bmi, name):
            val = bmi.get_value(name)
            dtype = bmi.get_var_type(name)
            assert_equal(dtype, type(val.flatten()[0]).__name__)
        _check_var_type.description = "Test get_var_type for {name}".format(name=name)

        yield _check_var_type, bmi, name


@with_setup(setup_func, teardown_func)
def test_get_var_units():
    """Test the units of the variables."""
    bmi = new_bmi()
    for name in all_names(bmi):
        units = bmi.get_var_units(name)
        def _check_units_is_str(units):
            assert_is_instance(units, str)
        def _check_units_is_valid(units):
            cfunits.Units(units)
        _check_units_is_str.description = "Test units for {name} is str".format(name=name)
        _check_units_is_valid.description = "Test units for {name} is valid".format(name=name)

        yield _check_units_is_str, units
        yield _check_units_is_valid, units

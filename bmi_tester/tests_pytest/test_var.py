import numpy as np

import cfunits


def test_get_var_grid(new_bmi, var_name):
    """Test the grid of the variables."""
    gid = new_bmi.get_var_grid(var_name)
    assert isinstance(gid, int)


def test_get_var_itemsize(new_bmi, var_name):
    """Test getting a variable's itemsize"""
    itemsize = new_bmi.get_var_itemsize(var_name)
    assert itemsize > 0


def test_get_var_nbytes(new_bmi, var_name):
    """Test getting a variable's nbytes"""
    nbytes = new_bmi.get_var_nbytes(var_name)
    assert nbytes > 0


def test_get_var_type(new_bmi, var_name):
    """Test getting a variable's data type"""
    dtype = new_bmi.get_var_type(var_name)
    try:
        np.empty(1, dtype=dtype)
    except TypeError:
        raise AssertionError(
            "get_var_type: bad data type name ({dtype})".format(dytpe=dtype)
        )


def test_get_var_units(new_bmi, var_name):
    """Test the units of the variables."""
    units = new_bmi.get_var_units(var_name)
    assert isinstance(units, str)
    cfunits.Units(units)

import numpy as np

from pymt import cfunits


def test_get_var_grid(initialized_bmi, var_name):
    """Test the grid of the variables."""
    gid = initialized_bmi.get_var_grid(var_name)
    assert isinstance(gid, int)


def test_get_var_itemsize(initialized_bmi, var_name):
    """Test getting a variable's itemsize"""
    itemsize = initialized_bmi.get_var_itemsize(var_name)
    assert itemsize > 0


def test_get_var_nbytes(initialized_bmi, var_name):
    """Test getting a variable's nbytes"""
    nbytes = initialized_bmi.get_var_nbytes(var_name)
    assert nbytes > 0


def test_get_var_type(initialized_bmi, var_name):
    """Test getting a variable's data type"""
    dtype = initialized_bmi.get_var_type(var_name)
    try:
        np.empty(1, dtype=dtype)
    except TypeError:
        raise AssertionError(
            "get_var_type: bad data type name ({dtype})".format(dtype=dtype)
        )


def test_get_var_units(initialized_bmi, var_name):
    """Test the units of the variables."""
    units = initialized_bmi.get_var_units(var_name)
    assert isinstance(units, str)
    cfunits.Units(units)

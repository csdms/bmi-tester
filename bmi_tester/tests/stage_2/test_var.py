import numpy as np
import pytest

from bmi_tester.units import Units

# try:
#     from pymt import cfunits
# except (FileNotFoundError, ModuleNotFoundError):
#     cfunits = None


# @pytest.mark.dependency()
# @pytest.mark.dependency(depends=["test_get_var_location"])
# def test_get_var_grid(initialized_bmi, var_name):
#     """Test the grid of the variables."""
#     if initialized_bmi.get_var_location(var_name) == "none":
#         pytest.skip(f"var, {var_name}, is not located on a grid")
#
#     gid = initialized_bmi.get_var_grid(var_name)
#     assert isinstance(gid, int)


def test_get_var_itemsize(initialized_bmi, var_name):
    """Test getting a variable's itemsize"""
    itemsize = initialized_bmi.get_var_itemsize(var_name)
    assert itemsize > 0


# @pytest.mark.dependency()
def test_get_var_nbytes(initialized_bmi, var_name):
    """Test getting a variable's nbytes"""
    nbytes = initialized_bmi.get_var_nbytes(var_name)
    assert nbytes > 0


# @pytest.mark.dependency()
def test_get_var_location(initialized_bmi, var_name):
    """Test getting a variable's grid location"""
    location = initialized_bmi.get_var_location(var_name)
    assert isinstance(location, str)
    assert location in ("node", "edge", "face", "none")


# @pytest.mark.dependency(depends=["test_get_var_location"])
def test_var_on_grid(initialized_bmi, var_name):
    loc = initialized_bmi.get_var_location(var_name)
    if initialized_bmi.get_var_location(var_name) == "none":
        pytest.skip(f"var, {var_name}, is not located on a grid")

    gid = initialized_bmi.get_var_grid(var_name)
    if loc == "node":
        assert initialized_bmi.get_grid_node_count(gid) > 0
    elif loc == "edge":
        assert initialized_bmi.get_grid_edge_count(gid) > 0
    elif loc == "face":
        assert initialized_bmi.get_grid_face_count(gid) > 0


def test_get_var_type(initialized_bmi, var_name):
    """Test getting a variable's data type"""
    dtype = initialized_bmi.get_var_type(var_name)
    assert isinstance(dtype, str)

    try:
        np.empty(1, dtype=dtype)
    except TypeError:
        raise AssertionError(
            "get_var_type: bad data type name ({dtype})".format(dtype=dtype)
        )


# @pytest.mark.skipif(cfunits is None, reason="cfunits is broken on this platform")
def test_get_var_units(initialized_bmi, var_name):
    """Test the units of the variables."""
    units = initialized_bmi.get_var_units(var_name)
    assert isinstance(units, str)
    unit_system = Units()
    assert unit_system.is_valid(units)
    # cfunits.Units(units)

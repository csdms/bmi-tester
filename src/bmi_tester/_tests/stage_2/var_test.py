import numpy as np
import pytest

from bmi_tester.api import WITH_GIMLI_UNITS
from bmi_tester.api import check_unit_is_valid


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
    if initialized_bmi.get_grid_type(gid) == "unstructured":
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
        raise AssertionError(f"get_var_type: bad data type name ({dtype})")


@pytest.mark.skipif(not WITH_GIMLI_UNITS, reason="gimli.units is not installed")
def test_get_var_units(initialized_bmi, var_name):
    """Test the units of the variables."""
    units = initialized_bmi.get_var_units(var_name)
    assert isinstance(units, str)
    assert check_unit_is_valid(units)

def test_set_get_interaction(initialized_bmi):
    """Test fundmanetal state behaviour of every output variable which is also an input variable:"""

    # Take the intersection of output and input vars
    for var_name in initialized_bmi.get_output_var_names():
      if var_name in initialized_bmi.get_input_var_names():

        # Get the variables type
        ty = np.dtype(initialized_bmi.get_var_type(var_name))
        # Generate some systematic test cases for this variable's type
        zero = np.zeros(1, dtype=ty)
        one  = np.ones(1, dtype=ty)
        for val in [zero, one, one + one]:
          # Test set-get behaviour
          # (i.e., setting a value then getting it produces the same result)
          initialized_bmi.set_value(var_name, val)
          val_out = initialized_bmi.get_value(var_name)
          assert val_out == val

          # Test set-set-get behaviour
          # (i.e., setting is idempotent; setting twice has no visible effect)
          initialized_bmi.set_value(var_name, val)
          val_out_again = initialized_bmi.get_value(var_name)
          assert val_out_again == val_out
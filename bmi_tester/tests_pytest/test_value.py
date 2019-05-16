from __future__ import print_function

import warnings
from distutils.version import StrictVersion

import numpy as np
import pytest

from .conftest import BMI_VERSION_STRING, INPUT_FILE, Bmi

BMI_VERSION = StrictVersion(BMI_VERSION_STRING)

BAD_VALUE = {"f": np.nan, "i": -999, "u": 0}


def empty_var_buffer(bmi, var_name):
    gid = bmi.get_var_grid(var_name)
    if BMI_VERSION > "1.0":
        loc = bmi.get_var_location(var_name)
    else:
        warnings.warn(
            "get_var_location not implemented (assuming nodes)", FutureWarning
        )
        loc = "node"

    if loc == "node":
        size = bmi.get_grid_size(gid)
    elif loc == "edge":
        size = bmi.get_grid_edge_count(gid)
    elif loc == "face":
        size = bmi.get_grid_face_count(gid)
    else:
        size = 0

    dtype = np.dtype(bmi.get_var_type(var_name))
    values = np.empty(size, dtype=dtype)

    return values


def test_get_var_location(initialized_bmi, var_name):
    """Test for get_var_location"""
    if BMI_VERSION < "1.1":
        pytest.skip(
            "testing BMIv{ver}: get_var_location was introduced in BMIv1.1".format(
                ver=BMI_VERSION
            )
        )

    assert hasattr(initialized_bmi, "get_var_location")

    loc = initialized_bmi.get_var_location(var_name)

    assert isinstance(loc, str)
    assert loc in ("node", "edge", "face")


def test_get_input_values(staged_tmpdir, in_var_name):
    """Input values are numpy arrays."""
    with staged_tmpdir.as_cwd():
        bmi = Bmi()
        bmi.initialize(INPUT_FILE)

        values = empty_var_buffer(bmi, in_var_name)
        values.fill(BAD_VALUE[values.dtype.kind])
        rtn = bmi.set_value(in_var_name, values)
        if rtn is None:
            warnings.warn("set_value should return the buffer")
        else:
            assert values is rtn
        if np.isnan(BAD_VALUE[values.dtype.kind]):
            assert np.all(np.isnan(values))
        else:
            assert np.all(values == BAD_VALUE[values.dtype.kind])


def test_get_output_values(initialized_bmi, out_var_name):
    """Output values are numpy arrays."""
    values = empty_var_buffer(initialized_bmi, out_var_name)
    values.fill(BAD_VALUE[values.dtype.kind])
    initial = values.copy()
    try:
        rtn = initialized_bmi.get_value(out_var_name, values)
    except TypeError:
        warnings.warn("get_value should take two arguments")
        rtn = initialized_bmi.get_value(out_var_name)
        values[:] = rtn
    else:
        assert values is rtn

    assert np.any(values != initial)

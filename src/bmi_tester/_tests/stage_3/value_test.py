import numpy as np
import pytest
from numpy.testing import assert_array_equal


def test_set_input_values(staged_tmpdir, bmi_factory, bmi_config, in_var_name):
    """Input values are numpy arrays."""
    with staged_tmpdir.as_cwd():
        bmi = bmi_factory()
        bmi.initialize(bmi_config.input_file)

        try:
            if in_var_name not in bmi.get_output_var_names():
                pytest.skip(f"{in_var_name}: no readable current value for this input")

            nbytes = bmi.get_var_nbytes(in_var_name)
            dtype = np.dtype(bmi.get_var_type(in_var_name))
            itemsize = bmi.get_var_itemsize(in_var_name)

            assert nbytes % dtype.itemsize == 0
            assert dtype.itemsize == itemsize

            n_items = nbytes // dtype.itemsize

            initial_array = np.empty(n_items, dtype=dtype)
            assert bmi.get_value(in_var_name, initial_array) is initial_array

            array = initial_array.copy()
            assert bmi.set_value(in_var_name, array) is None
            assert_array_equal(array, initial_array)
        finally:
            bmi.finalize()


def test_get_output_values(initialized_bmi, out_var_name):
    """Output values are numpy arrays."""
    nbytes = initialized_bmi.get_var_nbytes(out_var_name)
    dtype = np.dtype(initialized_bmi.get_var_type(out_var_name))
    itemsize = initialized_bmi.get_var_itemsize(out_var_name)

    assert nbytes % dtype.itemsize == 0
    assert dtype.itemsize == itemsize

    n_items = nbytes // dtype.itemsize

    first = np.zeros(n_items, dtype=dtype)
    second = np.ones(n_items, dtype=dtype)

    assert initialized_bmi.get_value(out_var_name, first) is first
    assert initialized_bmi.get_value(out_var_name, second) is second

    np.testing.assert_array_equal(first, second)

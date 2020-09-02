from distutils.version import StrictVersion

import numpy as np
import pytest
# from pytest_dependency import depends

from bmi_tester.api import empty_var_buffer

from ..conftest import BMI_VERSION_STRING, INPUT_FILE, Bmi

BMI_VERSION = StrictVersion(BMI_VERSION_STRING)

BAD_VALUE = {"f": np.nan, "i": -999, "u": 0}


# @pytest.mark.dependency()
# def test_get_var_location(var_name):
#     if var_name == "channel_entrance_water_sediment~bedload__mass_flow_rate":
#         assert False


# @pytest.mark.dependency()
def test_get_var_location(initialized_bmi, var_name):
    """Test for get_var_location"""
    # assert False
    if BMI_VERSION < "1.1":
        pytest.skip(
            "testing BMIv{ver}: get_var_location was introduced in BMIv1.1".format(
                ver=BMI_VERSION
            )
        )

    assert hasattr(initialized_bmi, "get_var_location")

    loc = initialized_bmi.get_var_location(var_name)

    assert isinstance(loc, str)
    assert loc in ("node", "edge", "face", "none")


# @pytest.mark.dependency(depends=["initialize_works", "test_get_var_grid", "get_var_nbytes"], scope="session")
def test_set_input_values(staged_tmpdir, in_var_name):
    """Input values are numpy arrays."""
    with staged_tmpdir.as_cwd():
        bmi = Bmi()
        bmi.initialize(INPUT_FILE)

        values = empty_var_buffer(bmi, in_var_name)
        # values.fill(BAD_VALUE[values.dtype.kind])
        bmi.set_value(in_var_name, values)

        # if np.isnan(BAD_VALUE[values.dtype.kind]):
        #     assert np.all(np.isnan(values))
        # else:
        #     assert np.all(values == BAD_VALUE[values.dtype.kind])


# @pytest.mark.dependency(depends=["initialize_works", "test_get_var_grid", "get_var_nbytes"], scope="session")
# @pytest.mark.dependency(depends=["initialize_works"], scope="session")
# @pytest.mark.dependency(depends=["test_get_var_location"])
def test_get_output_values(request, initialized_bmi, out_var_name):
    """Output values are numpy arrays."""
    # name = "../../../../../../../Users/huttone/git/csdms/bmi-tester/bmi_tester/tests_pytest/test_var.py::test_get_var_grid[%s]" % out_var_name
    # depends(request, ["test_get_var_location[%s]" % out_var_name])

    # depends(request, [name])
    # depends(request, ["test_var.py::test_get_var_grid[%s]" % out_var_name]) # , "test_get_var_nbytes[%s]" % out_var_name], scope="session")

    # depends(initialized_bmi, ["test_get_var_grid[%s]" % out_var_name, "test_get_var_nbytes" % out_var_name], scope="session")

    values = empty_var_buffer(initialized_bmi, out_var_name)
    # values.fill(BAD_VALUE[values.dtype.kind])
    initial = values.tobytes()
    initialized_bmi.get_value(out_var_name, values)

    assert initial != values.tobytes()
    # assert np.any(values != initial)

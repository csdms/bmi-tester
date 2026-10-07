import contextlib
import os

import numpy as np
import pytest
from packaging.version import Version


@contextlib.contextmanager
def suppress_stdout():
    null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
    # Save the actual stdout (1) and stderr (2) file descriptors.
    save_fds = [os.dup(1), os.dup(2)]

    os.dup2(null_fds[0], 1)
    os.dup2(null_fds[1], 2)

    yield

    # Re-assign the real stdout/stderr back to (1) and (2)
    os.dup2(save_fds[0], 1)
    os.dup2(save_fds[1], 2)
    # Close the null files
    for fd in null_fds + save_fds:
        os.close(fd)


def empty_var_buffer(bmi, var_name):
    """Create an empty value buffer for a BMI variable.

    Examples
    --------
    >>> import numpy as np
    >>> from bmi_tester._utils import empty_var_buffer

    >>> class Bmi:
    ...     def get_var_nbytes(self, name):
    ...         return 128
    ...     def get_var_type(self, name):
    ...         return "int"

    >>> buffer = empty_var_buffer(Bmi(), "var-name")
    >>> np.any(buffer != 0)
    True
    >>> buffer[:] = 0
    >>> np.all(buffer == 0)
    True
    """
    nbytes = bmi.get_var_nbytes(var_name)
    dtype = np.dtype(bmi.get_var_type(var_name))

    values = np.frombuffer(np.random.bytes(nbytes), dtype=dtype).copy()

    return values


def skip_if_not_bmi_2(bmi_version):
    if bmi_version < Version("2.0"):
        pytest.skip(f"{bmi_version}: BMI version is less than 2.0")


def skip_if_grid_type_is_not(bmi, gid, gtype):
    if isinstance(gtype, str):
        gtype = (gtype,)
    if bmi.get_grid_type(gid) not in gtype:
        gtypes = ", ".join(gtype)
        if len(gtype) > 1:
            pytest.skip(f"grid {gid} is not one of {gtypes}")
        else:
            pytest.skip(f"grid {gid} is not {gtypes}")


def skip_if_grid_type_is(bmi, gid, gtype):
    if isinstance(gtype, str):
        gtype = (gtype,)
    if bmi.get_grid_type(gid) in gtype:
        gtypes = ", ".join(gtype)
        if len(gtype) > 1:
            pytest.skip(f"grid {gid} is one of {gtypes}")
        else:
            pytest.skip(f"grid {gid} is {gtypes}")


def all_grids(bmi, gtype=None):
    in_names = set(bmi.get_input_var_names())
    out_names = set(bmi.get_output_var_names())

    grids = set()
    for name in in_names | out_names:
        if bmi.get_var_location(name) != "none":
            gid = bmi.get_var_grid(name)
            if gtype == bmi.get_grid_type(gid) or gtype is None:
                grids.add(gid)
    return grids

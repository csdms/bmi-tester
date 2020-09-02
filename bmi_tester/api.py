import contextlib
import ctypes
import ctypes.util
import os
import sys

import numpy as np
import pkg_resources
import pytest
import six


def check_bmi(
    package,
    tests_dir=None,
    input_file=None,
    manifest=None,
    bmi_version="1.1",
    extra_args=None,
    help_pytest=False,
):
    if tests_dir is None:
        tests_dir = pkg_resources.resource_filename(__name__, "bootstrap")
    args = [tests_dir]

    os.environ["BMITEST_CLASS"] = package
    os.environ["BMITEST_INPUT_FILE"] = input_file or ""
    os.environ["BMI_VERSION_STRING"] = bmi_version

    if manifest:
        if isinstance(manifest, six.string_types):
            with open(manifest, "r") as fp:
                manifest = fp.read()
        else:
            manifest = os.linesep.join(manifest)
        os.environ["BMITEST_MANIFEST"] = manifest

    extra_args = extra_args or []
    if help_pytest:
        extra_args.append("--help")
    args += extra_args

    return pytest.main(args)


@contextlib.contextmanager
def suppress_stdout(streams):
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
    >>> from bmi_tester.api import empty_var_buffer

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


def check_units(units):
    path_to_udunits_lib = ctypes.util.find_library("udunits2")
    udunits = ctypes.CDLL(path_to_udunits_lib)

    ut_read_xml = udunits.ut_read_xml
    ut_read_xml.argtypes = (ctypes.c_char_p, )
    ut_read_xml.restype = ctypes.c_void_p

    ut_parse = udunits.ut_parse
    ut_parse.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int)
    ut_parse.restype = ctypes.c_void_p

    with suppress_stdout(sys.stderr):
        ut_system = ut_read_xml(None)
    return ut_parse(ut_system, units.encode("utf-8"), 0) is not None

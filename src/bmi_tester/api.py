import contextlib
import os

import gimli
import numpy as np
import pkg_resources
import pytest

SECONDS = gimli.units.Unit("s")


def check_bmi(
    package,
    tests_dir=None,
    input_file=None,
    manifest=None,
    bmi_version="2.0",
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
        if isinstance(manifest, str):
            with open(manifest) as fp:
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


def check_unit_is_valid(unit):
    try:
        gimli.units.Unit(unit)
    except gimli.UnitNameError:
        return False
    else:
        return True


def check_unit_is_time(unit):
    try:
        gimli.units.Unit(unit).to(SECONDS)
    except gimli.IncompatibleUnitsError:
        return False
    else:
        return True


def check_unit_is_dimensionless(unit):
    return gimli.units.Unit(unit).is_dimensionless

import os
import sys
from collections.abc import Iterable
from collections.abc import Sequence

try:
    import gimli
except ImportError:
    WITH_GIMLI_UNITS = False
    SECONDS = None
else:
    WITH_GIMLI_UNITS = True
    SECONDS = gimli.units.Unit("s")

import pytest

if sys.version_info >= (3, 12):  # pragma: no cover (PY12+)
    from importlib.resources import files
else:  # pragma: no cover (<PY312)
    from importlib_resources import files


def check_bmi(
    package: str,
    tests_dir: str | Sequence[str] | None = None,
    input_file: str = "",
    manifest: str | Sequence[str] | None = None,
    bmi_version: str = "2.0",
    extra_args: Iterable[str] | None = None,
    help_pytest: bool = False,
) -> int:
    if tests_dir is None:
        tests_dir = str(files(__name__) / "_bootstrap")
    if isinstance(tests_dir, str):
        args = [tests_dir]
    else:
        args = list(tests_dir)

    os.environ["BMITEST_CLASS"] = package
    os.environ["BMITEST_INPUT_FILE"] = input_file
    os.environ["BMI_VERSION_STRING"] = bmi_version

    if manifest:
        if isinstance(manifest, str):
            with open(manifest) as fp:
                manifest = fp.read()
        else:
            manifest = os.linesep.join(manifest)
        os.environ["BMITEST_MANIFEST"] = manifest

    extra_args = list(extra_args or [])
    if help_pytest:
        extra_args.append("--help")
    args += extra_args
    return pytest.main(args)


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

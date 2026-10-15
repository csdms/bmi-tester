import os
import sys
from collections.abc import Iterable
from collections.abc import Sequence

try:
    from gimli import units
except ImportError:
    WITH_GIMLI_UNITS = False
else:
    WITH_GIMLI_UNITS = True

import pytest
from pytest import ExitCode

from bmi_tester._pytest import BmiPlugin
from bmi_tester._pytest import RunConfig

if sys.version_info >= (3, 12):  # pragma: no cover (PY12+)
    from importlib.resources import files
else:  # pragma: no cover (<PY312)
    from importlib_resources import files


def check_bmi(
    package: str,
    *,
    test_dirs: str | Sequence[str] | None = None,
    input_file: str = "",
    manifest: str | Sequence[str] | None = None,
    bmi_version: str = "2.0",
    extra_args: Iterable[str] | None = None,
    help_pytest: bool = False,
    stop_on_stage_failure: bool = True,
) -> int:
    """Run pytest checks against a BMI implementation.

    Parameters
    ----------
    package : str
        Model entry point in ``module:Class`` form, such as
        ``testing.bmi:BmiExample``.
    test_dirs : str or sequence of str, optional
        Test paths to pass to pytest. Defaults to the complete set of bundled
        checks.
    input_file : str, optional
        Configuration filename passed to the model's ``initialize`` method.
        Defaults to an empty string.
    manifest : str or sequence of str, optional
        Path to a text file listing one model input file per line, or a
        sequence of input filenames. Paths are relative to the current
        working directory, not the manifest file's directory. These files
        are copied into temporary directories for tests that request staged
        inputs. Leading and trailing whitespace and blank entries are ignored.
        If None or an empty string, use ``input_file`` when it is nonempty.
        An empty sequence stages no files.
    bmi_version : str, optional
        BMI specification version to test against. Defaults to ``"2.0"``.
    extra_args : iterable of str, optional
        Additional command-line arguments passed to pytest.
    help_pytest : bool, optional
        If True, append ``--help`` to the pytest arguments to display pytest
        help instead of running tests. Defaults to False.
    stop_on_stage_failure : bool, optional
        Stop execution if a stage fails.

    Returns
    -------
    int
        Pytest exit code: zero for success and nonzero for test failures
        or other pytest errors.

    Notes
    -----
    Each invocation registers a fresh BMI plugin with its own configuration
    and cached model metadata. Configuration is not read from or written to
    environment variables. Model inputs must be accessible from the current
    working directory; parameter discovery initializes a model there.
    """
    if test_dirs is None:
        test_dirs = [
            str(files(__name__) / stage)
            for stage in (
                "_bootstrap",
                "_tests/stage_1",
                "_tests/stage_2",
                "_tests/stage_3",
            )
        ]
    elif isinstance(test_dirs, str):
        test_dirs = [test_dirs]

    if isinstance(manifest, str) and manifest:
        with open(manifest) as fp:
            manifest = fp.read().splitlines()
    elif manifest is None or manifest == "":
        manifest = [input_file]

    config = RunConfig(
        entry_point=package,
        input_file=input_file,
        manifest=tuple(name.strip() for name in manifest if name.strip()),
        bmi_version=bmi_version,
    )

    extra_args = tuple(extra_args or ())
    if help_pytest:
        return pytest.main(["--help", *extra_args], plugins=[BmiPlugin(config)])

    stage_status = {}
    for stage_dir in map(os.path.abspath, test_dirs):
        if stage_dir in stage_status:
            continue

        status = pytest.main([stage_dir, *extra_args], plugins=[BmiPlugin(config)])
        stage_status[stage_dir] = status
        if status != ExitCode.OK and stop_on_stage_failure:
            break

    failed_stages = [
        stage for stage, status in stage_status.items() if status != ExitCode.OK
    ]

    return stage_status[failed_stages[0]] if failed_stages else ExitCode.OK


def check_unit_is_valid(unit):
    if not WITH_GIMLI_UNITS:
        raise ImportError(
            "Unit validation requires gimli.units."
            " Install it with: pip install 'bmi-tester[units]'"
        )

    return unit in units


def check_unit_is_time(unit):
    if not WITH_GIMLI_UNITS:
        raise ImportError(
            "Unit validation requires gimli.units."
            " Install it with: pip install 'bmi-tester[units]'"
        )

    return unit in units and (
        units[unit].is_convertible_to(units["s"])
        or units[unit].is_convertible_to(units["seconds since 1969-07-20 20:17:40 UTC"])
    )


def check_unit_is_dimensionless(unit):
    if not WITH_GIMLI_UNITS:
        raise ImportError(
            "Unit validation requires gimli.units."
            " Install it with: pip install 'bmi-tester[units]'"
        )

    return unit in units and units[unit].is_dimensionless

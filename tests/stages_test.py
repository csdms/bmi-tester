import os
from unittest.mock import patch

import pytest
from pytest import ExitCode

import bmi_tester
from bmi_tester.main import run_the_tests


@pytest.mark.parametrize(
    "stages, expected",
    [
        (None, ["_bootstrap", "stage_1", "stage_2", "stage_3"]),
        (["2", "3"], ["stage_2", "stage_3"]),
    ],
)
def test_cli_delegates_stage_execution(stages, expected):
    with patch.object(
        bmi_tester.main, "check_bmi", autospec=True, return_value=ExitCode.TESTS_FAILED
    ) as check_bmi:
        assert (
            run_the_tests(
                "example:Model",
                "config.yaml",
                ("config.yaml",),
                bmi_version="1.0",
                pytest_help=True,
                stages=stages,
            )
            == ExitCode.TESTS_FAILED
        )

    assert check_bmi.call_count == 1
    assert check_bmi.call_args.args == ("example:Model",)

    kwds = dict(check_bmi.call_args.kwargs)

    stages = [os.path.basename(path) for path in kwds.pop("test_dirs")]
    assert stages == expected

    assert kwds == {
        "input_file": "config.yaml",
        "manifest": ("config.yaml",),
        "bmi_version": "1.0",
        "help_pytest": True,
        "stop_on_stage_failure": True,
    }

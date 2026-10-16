import os
from unittest.mock import patch

import pytest
from pytest import ExitCode

import bmi_tester
from bmi_tester._pytest import RunConfig
from bmi_tester.api import check_bmi


@pytest.fixture
def pytest_main():
    with patch.object(pytest, "main", return_value=ExitCode.OK) as runner:
        yield runner


def touch_file(fname):
    with open(fname, "w"):
        pass


def test_bmi_check(tmpdir):
    with tmpdir.as_cwd():
        touch_file("input.yaml")
        assert (
            check_bmi(
                "testing.uniform_rectilinear_bmi:UniformRectilinearBmi",
                input_file="input.yaml",
                extra_args=["-vvv"],
            )
            == 0
        )


def test_bmi_check_with_manifest_as_list(tmpdir):
    with tmpdir.as_cwd():
        touch_file("input.yaml")
        assert (
            check_bmi(
                "testing.uniform_rectilinear_bmi:UniformRectilinearBmi",
                extra_args=["-vvv"],
                input_file="input.yaml",
                manifest=["input.yaml"],
            )
            == 0
        )


def test_bmi_check_with_manifest_as_string(tmpdir):
    with tmpdir.as_cwd():
        with open("manifest.txt", "w") as fp:
            fp.write(os.linesep.join(["input.yaml", "data.dat"]))
        touch_file("input.yaml")
        touch_file("data.dat")
        assert (
            check_bmi(
                "testing.uniform_rectilinear_bmi:UniformRectilinearBmi",
                extra_args=["-vvv"],
                input_file="input.yaml",
                manifest="manifest.txt",
            )
            == 0
        )


def test_default_stage_order_and_configuration(pytest_main):
    assert (
        check_bmi(
            "example:Model",
            input_file="config.yaml",
            bmi_version="1.0",
            extra_args=("--quiet",),
        )
        == ExitCode.OK
    )

    root = os.path.dirname(bmi_tester.__file__)

    expected = [
        "_bootstrap",
        *[os.path.join("_tests", f"stage_{n}") for n in (1, 2, 3)],
    ]

    actual = [call.args[0][0] for call in pytest_main.call_args_list]

    assert actual == [os.path.join(root, p) for p in expected]

    actual = [call.args[0][1] for call in pytest_main.call_args_list]
    assert actual == ["--quiet"] * 4

    plugins = [call.kwargs["plugins"][0] for call in pytest_main.call_args_list]
    assert len({id(plugin) for plugin in plugins}) == 4

    expected = RunConfig(
        entry_point="example:Model",
        input_file="config.yaml",
        manifest=("config.yaml",),
        bmi_version="1.0",
    )

    assert [plugin.config for plugin in plugins] == [expected] * 4


@pytest.mark.parametrize("failure", [ExitCode.TESTS_FAILED, ExitCode.USAGE_ERROR])
def test_stop_after_failed_stage(pytest_main, failure):
    pytest_main.side_effect = [ExitCode.OK, failure, ExitCode.OK]
    assert check_bmi("example:Model", test_dirs=["first", "second", "third"]) == failure

    stages = [os.path.basename(call.args[0][0]) for call in pytest_main.call_args_list]
    assert "third" not in stages
    assert stages == ["first", "second"]


@pytest.mark.parametrize(
    "statuses",
    [
        [ExitCode.TESTS_FAILED, ExitCode.USAGE_ERROR, ExitCode.OK],
        [ExitCode.OK, ExitCode.INTERNAL_ERROR, ExitCode.TESTS_FAILED],
    ],
)
def test_continue_preserves_first_failure(pytest_main, statuses):
    pytest_main.side_effect = statuses

    first_failure = [status for status in statuses if status != ExitCode.OK][0]
    assert (
        check_bmi(
            "example:Model",
            test_dirs=["first", "second", "third"],
            stop_on_stage_failure=False,
        )
        == first_failure
    )

    assert pytest_main.call_count == 3


def test_single_test_path(pytest_main):
    assert check_bmi("example:Model", test_dirs="foo") == ExitCode.OK
    assert pytest_main.call_count == 1
    assert pytest_main.call_args.args[0] == [os.path.abspath("foo")]


def test_duplicate_paths_run_once(pytest_main):
    assert (
        check_bmi("example:Model", test_dirs=["first", "./first", "second"])
        == ExitCode.OK
    )
    stages = [os.path.basename(call.args[0][0]) for call in pytest_main.call_args_list]
    assert stages == ["first", "second"]


def test_help_runs_once_without_stages(pytest_main):
    pytest_main.return_value = ExitCode.USAGE_ERROR
    assert (
        check_bmi("example:Model", help_pytest=True, extra_args=["-q"])
        == ExitCode.USAGE_ERROR
    )
    assert pytest_main.call_count == 1
    assert pytest_main.call_args.args[0] == ["--help", "-q"]


def test_empty_stages(pytest_main):
    assert check_bmi("example:Model", test_dirs=[]) == ExitCode.OK
    pytest_main.assert_not_called()

import os
import pkg_resources
import pytest


def check_bmi(
    package,
    input_file=None,
    manifest=None,
    bmi_version="1.1",
    extra_args=None,
    help_pytest=False,
):
    args = [pkg_resources.resource_filename(__name__, os.path.join("tests_pytest"))]
    os.environ["BMITEST_CLASS"] = package
    os.environ["BMITEST_INPUT_FILE"] = input_file
    os.environ["BMI_VERSION_STRING"] = bmi_version

    if manifest is not None:
        with open(manifest, "r") as fp:
            manifest = fp.read()
        os.environ["BMITEST_MANIFEST"] = manifest

    extra_args = extra_args or []
    if help_pytest:
        extra_args.append("--help")
    args += extra_args

    print("Running: {0}".format(" ".join(args)))
    return pytest.main(args)



from __future__ import print_function

import os
import sys

import pkg_resources
import pytest
import six


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

    print("Running: {0}".format(" ".join(args)), file=sys.stderr)
    return pytest.main(args)

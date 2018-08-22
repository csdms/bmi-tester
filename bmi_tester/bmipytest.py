#! /usr/bin/env python
from __future__ import print_function

import os
import sys
import textwrap
import argparse

import pkg_resources
import pytest


def test(
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


def configure_parser_test(sub_parsers=None):
    help = "Test a BMI class."

    example = textwrap.dedent(
        """

    Examples:

    bmi test bmimodule:BmiClass
    """
    )

    if sub_parsers is None:
        p = argparse.ArgumentParser(
            description=help,
            fromfile_prefix_chars="@",
            epilog=example,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    else:
        p = sub_parsers.add_parser(
            "test",
            help=help,
            description=help,
            epilog=example,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    p.add_argument("cls", help="Full name of class to test.")
    p.add_argument("--infile", default="", help="Name of input file for init method.")
    p.add_argument(
        "--manifest", default="", type=str, help="Name of manifest file of input files."
    )
    p.add_argument("--bmi-version", default="1.1", help="BMI version to test against")
    p.add_argument("--help-pytest", action="store_true", help="Print help for pytest")
    p.set_defaults(func=execute)

    return p


def execute(args, extra):
    return test(
        args.cls,
        input_file=args.infile,
        manifest=args.manifest,
        bmi_version=args.bmi_version,
        extra_args=extra,
        help_pytest=args.help_pytest,
    )


def main():
    p = configure_parser_test()

    args, extra = p.parse_known_args()

    sys.exit(args.func(args, extra))

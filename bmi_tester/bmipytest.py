#! /usr/bin/env python
import os
import sys
import textwrap
import argparse

import pkg_resources
import pytest


def test(package, input_file=None, manifest=None, verbosity=None, bmi_version="1.1"):
    tests = [pkg_resources.resource_filename(__name__, os.path.join("tests_pytest"))]
    os.environ["BMITEST_CLASS"] = package
    os.environ["BMITEST_INPUT_FILE"] = input_file
    os.environ["BMITEST_MANIFEST"] = manifest
    os.environ["BMI_VERSION_STRING"] = bmi_version

    if verbosity:
        tests += ["-" + "v" * verbosity]
    return pytest.main(tests)


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
    p.add_argument("--manifest", default="", type=str, help="Name of manifest file of input files.")
    p.add_argument("--bmi-version", default="1.1", help="BMI version to test against")
    p.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbose",
        default=1,
        help="increase verbosity",
    )
    p.add_argument(
        "--no-doctests",
        action="store_false",
        dest="doctests",
        default=True,
        help="Do not run doctests in module",
    )
    p.set_defaults(func=execute)

    return p


def execute(args):
    return test(
        args.cls,
        input_file=args.infile,
        manifest=args.manifest,
        verbosity=args.verbose,
        bmi_version=args.bmi_version,
    )


def main():
    p = configure_parser_test()

    args = p.parse_args()

    sys.exit(args.func(args))

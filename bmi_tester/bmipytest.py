#! /usr/bin/env python
from __future__ import print_function

import os
import sys
import textwrap
import argparse

from .api import check_bmi


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
    return check_bmi(
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

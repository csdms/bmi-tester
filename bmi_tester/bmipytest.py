#! /usr/bin/env python
from __future__ import print_function

import argparse
import sys
import tempfile
import textwrap

from model_metadata.api import query, stage
from scripting import cd

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
    p.add_argument(
        "--stage", action="store_true", help="Stage with defaults for testing"
    )
    p.set_defaults(func=execute)

    return p


def execute(args, extra):
    if args.stage:
        stage_dir = tempfile.mkdtemp()
        model = args.cls.split(":")[-1]
        input_file = query(model, "run.config_file.path")
        manifest = stage(model, stage_dir)
    else:
        input_file = args.infile
        manifest = args.manifest
        stage_dir = "."

    print("Running tests in {0}".format(stage_dir))
    with cd(stage_dir):
        return check_bmi(
            args.cls,
            input_file=input_file,
            manifest=manifest,
            bmi_version=args.bmi_version,
            extra_args=extra,
            help_pytest=args.help_pytest,
        )


def main():
    p = configure_parser_test()

    args, extra = p.parse_known_args()

    sys.exit(args.func(args, extra))

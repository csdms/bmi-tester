#! /usr/bin/env python
from __future__ import print_function

import argparse
import re
import sys
import tempfile
import textwrap

import click
from model_metadata.api import query, stage
from scripting import cd

from . import __version__
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


def validate_entry_point(ctx, param, value):
    MODULE_REGEX = r"^(?!.*\.\.)(?!.*\.$)[A-Za-z][\w\.]*$"
    CLASS_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
    if value is not None:
        try:
            module_name, class_name = value.split(":")
        except ValueError:
            raise click.BadParameter(
                "Bad entry point", param=value, param_hint="module_name:ClassName"
            )
        if not re.match(MODULE_REGEX, module_name):
            raise click.BadParameter(
                "Bad module name ({0})".format(module_name),
                param_hint="module_name:ClassName",
            )
        if not re.match(CLASS_REGEX, class_name):
            raise click.BadParameter(
                "Bad class name ({0})".format(class_name),
                param_hint="module_name:ClassName",
            )
    return value


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.version_option(version=__version__)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help=(
        "Don't emit non-error messages to stderr. Errors are still emitted, "
        "silence those with 2>/dev/null."
    ),
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Also emit status messages to stderr."
)
@click.option("--help-pytest", is_flag=True, help="Print help about pytest.")
@click.option(
    "--root-dir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, writable=True, resolve_path=True
    ),
    help="Define root directory for BMI tests",
)
@click.option("--config-file", help="Name to model configuration file")
@click.option(
    "--manifest",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
    help="Path to manifest file of staged model input files.",
)
@click.option("--bmi-version", default="1.1", help="BMI version to test against")
@click.argument("entry_point", callback=validate_entry_point)
@click.argument("pytest_args", nargs=-1, type=click.UNPROCESSED)
def main(
    entry_point,
    root_dir,
    bmi_version,
    config_file,
    manifest,
    quiet,
    verbose,
    pytest_args,
    help_pytest,
):
    module_name, class_name = entry_point.split(":")

    if root_dir is None:
        stage_dir = tempfile.mkdtemp()
        model = class_name
        config_file = query(model, "run.config_file.path")
        manifest = stage(model, stage_dir)
    else:
        stage_dir = root_dir

    print("Running tests in {0}".format(stage_dir))
    with cd(stage_dir):
        return check_bmi(
            entry_point,
            input_file=config_file,
            manifest=manifest,
            bmi_version=bmi_version,
            extra_args=pytest_args,
            help_pytest=help_pytest,
        )

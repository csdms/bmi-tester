#! /usr/bin/env python
from __future__ import print_function

import importlib
import re
import tempfile

import click

from model_metadata.api import query, stage
from scripting import cd

from . import __version__
from .api import check_bmi


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


def load_component(entry_point):
    module_name, cls_name = entry_point.split(":")

    component = None
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise
    else:
        try:
            component = module.__dict__[cls_name]
        except KeyError:
            raise ImportError(cls_name)

    return component


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
        # model = class_name
        model = load_component(entry_point)
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

#! /usr/bin/env python
import importlib
import os
import pathlib
import re
import sys
import tempfile
from functools import partial

import click
import pkg_resources
from model_metadata import MetadataNotFoundError
from model_metadata.api import query, stage
from pytest import ExitCode
from scripting import cd

from . import __version__
from .api import check_bmi

out = partial(click.secho, bold=True, err=True)
err = partial(click.secho, fg="red", err=True)


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
        #     component = module.__dict__[cls_name].__name__
        except KeyError:
            raise ImportError(cls_name)

    return component


def _stage_component(entry_point, stage_dir="."):
    config_file = query(entry_point, "run.config_file.path")
    manifest = stage(entry_point, str(stage_dir))

    return config_file, manifest


def _tree(files):
    tree = []
    prefix = ["|--"] * (len(files) - 1) + ["`--"]
    for p, fname in zip(prefix, files):
        tree.append(f"{p} {fname}")
    return os.linesep.join(tree)


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
@click.option(
    "--config-file",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, writable=True, resolve_path=True
    ),
    help="Name of model configuration file",
)
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
    """Validate a BMI implementation.

    \b
    Examples:

      Test a BMI for the class *Hydrotrend* in module *pymt_hydrotrend*,

        $ bmi-test pymt_hydrotrend:Hydrotrend

    This will test the BMI with a default set of input files as obtained
    through the model metadata associated with the component.

    If the component you would like to test does not have model metadata
    that bmi-tester recognizes, or you would like to test with a non-default
    set of input files, use the *--root-dir* and *--config-file* options.

        $ bmi-tests pymt_hydrotrend:Hydrotrend --root-dir=my_files/ --config-file=config.txt

    where *my_files* is a folder that contains the input files to test with
    and *config.txt* is the configuration file, which will be passed to the
    *initialize* method.
    """
    if root_dir and not config_file:
        err("using --root-dir but no config file specified (use --config-file)")
        raise click.Abort()

    module_name, class_name = entry_point.split(":")

    try:
        Bmi = load_component(entry_point)
    except ImportError:
        err(f"unable to import BMI implementation, {class_name}, from {module_name}")
        raise click.Abort()

    if root_dir:
        stage_dir = root_dir
        if manifest is None:
            manifest = os.listdir(stage_dir)
    else:
        stage_dir = tempfile.mkdtemp()
        try:
            config_file, manifest = _stage_component(entry_point, stage_dir)
        except MetadataNotFoundError:
            config_file, manifest = _stage_component(class_name, stage_dir)

    stages = sorted(
        [pathlib.Path(pkg_resources.resource_filename(__name__, "bootstrap"))]
        + list(
            pathlib.Path(pkg_resources.resource_filename(__name__, "tests")).glob(
                "stage_*"
            )
        )
    )

    if not quiet:
        out("Location of tests:")
        for stage_path in (str(stage_path) for stage_path in stages):
            out(f"- {stage_path}")
        out(f"Entry point: {entry_point}")
        out(repr(Bmi()))
        out(f"BMI version: {bmi_version}")
        out(f"Stage folder: {stage_dir}")
        out(f"> tree -d {stage_dir}")
        if manifest:
            out(_tree(manifest))
        out(f"> cat {stage_dir}/{config_file}")
        with open(os.path.join(stage_dir, config_file), "r") as fp:
            out(fp.read())

    with cd(stage_dir):
        for stage_path in sorted(stages):
            status = check_bmi(
                entry_point,
                tests_dir=str(stage_path),
                # tests_dir=tests_dir,
                input_file=config_file,
                manifest=manifest,
                bmi_version=bmi_version,
                extra_args=pytest_args + ("-vvv",),
                help_pytest=help_pytest,
            )
            if status != ExitCode.OK:
                break

    if not quiet:
        if status == ExitCode.OK:
            out("🎉 All tests passed!")
        else:
            err("😞 There were errors")

    sys.exit(status)

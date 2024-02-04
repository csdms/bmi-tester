from __future__ import annotations

import argparse
import os
import pathlib
import sys
import tempfile
from collections.abc import Iterator
from collections.abc import Sequence
from functools import partial
from typing import Any

from model_metadata._utils import as_cwd
from model_metadata._utils import load_component
from model_metadata._utils import parse_entry_point
from model_metadata.api import query
from model_metadata.api import stage
from model_metadata.errors import BadEntryPointError
from pytest import ExitCode

if sys.version_info >= (3, 12):  # pragma: no cover (PY12+)
    import importlib.resources as importlib_resources
else:  # pragma: no cover (<PY312)
    import importlib_resources

from bmi_tester._version import __version__
from bmi_tester.api import check_bmi

out = partial(print, file=sys.stderr)
err = partial(print, file=sys.stderr)


def main(argv: tuple[str, ...] | None = None) -> int:
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
    parser = argparse.ArgumentParser(prog="bmi-test")
    parser.add_argument(
        "--version", action="version", version=f"bmi-test {__version__}"
    )
    parser.add_argument("entry_point", action=ValidateEntryPoint)
    parser.add_argument(
        "--quiet",
        action="store_true",
        help=(
            "Don't emit non-error messages to stderr. Errors are still emitted, "
            "silence those with 2>/dev/null."
        ),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Also emit status messages to stderr.",
    )
    parser.add_argument(
        "--help-pytest", action="store_true", help="Print help about pytest."
    )
    parser.add_argument(
        "--root-dir",
        action=ValidatePathExists,
        help="Define root directory for BMI tests",
    )
    parser.add_argument(
        "--config-file",
        action=ValidatePathExists,
        help="Name of model configuration file",
    )
    parser.add_argument(
        "--manifest",
        action=ValidatePathExists,
        help="Path to manifest file of staged model input files.",
    )
    parser.add_argument(
        "--bmi-version", default="2.0", help="BMI version to test against"
    )

    args = parser.parse_args(argv)

    if args.root_dir:
        if not args.config_file:
            err("using --root-dir but no config file specified (use --config-file)")
            return -1

        stage = Stage(
            args.root_dir,
            config_file=args.config_file,
            manifest=args.manifest,
        )
    else:
        stage = Stage.from_entry_point(":".join(args.entry_point))

    with as_cwd(stage.dir):
        status = run_the_tests(
            ":".join(args.entry_point),
            stage.config_file,
            stage.manifest,
            bmi_version=args.bmi_version,
        )

    if not args.quiet:
        if status == ExitCode.OK:
            out("🎉 All tests passed!")
        else:
            err("😞 There were errors")

    return status


class Stage:
    def __init__(
        self,
        stage_dir: str,
        config_file: str,
        manifest: str | Iterator[str] | None = None,
    ):
        self._stage_dir = stage_dir
        self._config_file = config_file
        if manifest is None:
            manifest = stage_dir
        if isinstance(manifest, str):
            self._manifest = tuple(os.listdir(manifest))
        else:
            self._manifest = tuple(manifest)

    @property
    def dir(self) -> str:
        return self._stage_dir

    @property
    def manifest(self) -> tuple[str, ...]:
        return self._manifest

    @property
    def config_file(self) -> str:
        return self._config_file

    @classmethod
    def from_entry_point(cls, entry_point: str) -> Stage:
        module_name, class_name = parse_entry_point(entry_point)
        try:
            Bmi = load_component(module_name, class_name)
        except ImportError:
            err(
                f"unable to import BMI implementation, {class_name},"
                f" from {module_name}"
            )
            raise

        stage_dir = tempfile.mkdtemp()
        manifest = stage(Bmi, str(stage_dir))
        config_file = query(Bmi, "run.config_file.path")

        return cls(stage_dir, config_file=config_file, manifest=manifest)


def run_the_tests(
    entry_point: str,
    config_file: str,
    manifest: tuple[str, ...],
    bmi_version: str = "2.0",
    pytest_help: bool = False,
) -> int:
    path_to_tests = pathlib.Path(str(importlib_resources.files(__name__))).resolve()
    stages = [
        str(p)
        for p in [path_to_tests / "_bootstrap"]
        + sorted((path_to_tests / "_tests").glob("stage_*"))
    ]

    status = 0
    for stage_dir in stages:
        status = check_bmi(
            entry_point,
            tests_dir=stage_dir,
            input_file=config_file,
            manifest=manifest,
            bmi_version=bmi_version,
            # extra_args=pytest_args + ("-vvv",),
            help_pytest=pytest_help,
        )
        if status != ExitCode.OK:
            break

    return status


class ValidateEntryPoint(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        if not isinstance(values, str):
            parser.error(f"{values}: invalid entry-point: not a string")

        entry_point = values
        try:
            module_name, class_name = parse_entry_point(entry_point)
        except BadEntryPointError as error:
            parser.error(f"{entry_point}: invalid entry-point: {str(error)}")
        else:
            setattr(namespace, self.dest, (module_name, class_name))


class ValidatePathExists(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        if not isinstance(values, str):
            parser.error(f"{values}: invalid path: not a string")

        path = values

        # if not os.path.isdir(path):
        if not os.path.exists(path):
            parser.error(f"{path}: path does not exist")
        else:
            setattr(namespace, self.dest, path)


def _tree(files):
    tree = []
    prefix = ["|--"] * (len(files) - 1) + ["`--"]
    for p, fname in zip(prefix, files):
        tree.append(f"{p} {fname}")
    return os.linesep.join(tree)


if __name__ == "__main__":
    SystemExit(main())

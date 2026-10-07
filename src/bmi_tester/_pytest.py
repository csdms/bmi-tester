"""Fixtures and parametrization explicitly registered by check_bmi."""

import shutil
from dataclasses import dataclass
from pathlib import Path

import pytest
from model_metadata._utils import load_component
from model_metadata._utils import parse_entry_point
from packaging.version import Version

from bmi_tester._utils import all_grids


@dataclass(frozen=True)
class RunConfig:
    entry_point: str
    input_file: str
    manifest: tuple[str, ...]
    bmi_version: str


class BmiPlugin:
    def __init__(self, config: RunConfig):
        self.config = config
        self._component = None
        self._parameters = None

    @property
    def component(self):
        if self._component is None:
            module_name, class_name = parse_entry_point(self.config.entry_point)
            self._component = load_component(module_name, class_name)
        return self._component

    def pytest_generate_tests(self, metafunc):
        names = {"gid", "var_name", "in_var_name", "out_var_name"}
        requested = names.intersection(metafunc.fixturenames)
        if not requested:
            return
        if self._parameters is None:
            model = self.component()
            model.initialize(self.config.input_file)
            try:
                inputs = set(model.get_input_var_names())
                outputs = set(model.get_output_var_names())
                self._parameters = {
                    "gid": sorted(all_grids(model)),
                    "var_name": sorted(inputs | outputs),
                    "in_var_name": sorted(inputs),
                    "out_var_name": sorted(outputs),
                }
            finally:
                model.finalize()
        for name in sorted(requested):
            metafunc.parametrize(name, self._parameters[name], scope="session")

    @pytest.fixture(scope="session")
    def bmi_config(self):
        return self.config

    @pytest.fixture(scope="session")
    def bmi_version(self):
        return Version(self.config.bmi_version)

    @pytest.fixture(scope="session")
    def bmi_factory(self):
        return self.component

    @pytest.fixture(scope="session")
    def bmi(self):
        return self.component()

    def _stage(self, destination):
        for name in self.config.manifest:
            target = Path(str(destination)) / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(name, target)

    @pytest.fixture(scope="session")
    def initialized_bmi(self, tmpdir_factory):
        directory = tmpdir_factory.mktemp("data")
        self._stage(directory)
        with directory.as_cwd():
            model = self.component()
            model.initialize(self.config.input_file)
        try:
            yield model
        finally:
            with directory.as_cwd():
                model.finalize()

    @pytest.fixture
    def staged_tmpdir(self, tmpdir):
        self._stage(tmpdir)
        return tmpdir

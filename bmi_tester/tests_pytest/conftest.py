from __future__ import print_function
import os
import sys
import shutil

import pytest
# from scripting.contexts import cd, cp
from scripting import cd, cp

from . import Bmi, INPUT_FILE, MANIFEST
from .utils import all_grids, all_names, out_names, strictly_input_names


@pytest.fixture(scope="session")
def bmi(tmpdir_factory, infile=None):
    return Bmi()


@pytest.fixture(scope="session")
def initialized_bmi(tmpdir_factory, infile=None, manifest=None):
    infile = infile or INPUT_FILE
    manifest = manifest or MANIFEST
    with tmpdir_factory.as_cwd() as prev:
        for file_ in manifest:
            cp(os.path.join(prev, file_), file_, create_dirs=True)

        bmi = Bmi()
        with cd(root_dir):
            bmi.initialize(infile or INPUT_FILE)

    return bmi


@pytest.fixture
def staged_tmpdir(tmpdir, infile=None, manifest=None):
    infile = infile or INPUT_FILE
    manifest = manifest or MANIFEST
    with tmpdir.as_cwd() as prev:
        for file_ in manifest:
            cp(os.path.join(prev, file_), file_, create_dirs=True)
    return tmpdir


def pytest_generate_tests(metafunc):
    if "gid" in metafunc.fixturenames:
        metafunc.parametrize("gid", all_grids(new_bmi()))
    elif "var_name" in metafunc.fixturenames:
        metafunc.parametrize("var_name", all_names(new_bmi()))
    elif "in_var_name" in metafunc.fixturenames:
        metafunc.parametrize("in_var_name", strictly_input_names(new_bmi()))
    elif "out_var_name" in metafunc.fixturenames:
        metafunc.parametrize("out_var_name", out_names(new_bmi()))

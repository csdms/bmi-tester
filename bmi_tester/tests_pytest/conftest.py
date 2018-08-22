from __future__ import print_function
import os
import sys
import shutil

import pytest
# from scripting.contexts import cd, cp
from scripting import cd, cp

from . import Bmi, INPUT_FILE, MANIFEST
from .utils import get_test_parameters


@pytest.fixture(scope="session")
def bmi():
    return Bmi()


@pytest.fixture(scope="session")
def initialized_bmi(tmpdir_factory, infile=None, manifest=None):
    infile = infile or INPUT_FILE
    manifest = manifest or MANIFEST
    tmp = tmpdir_factory.mktemp("data")
    with tmp.as_cwd() as prev:
        for file_ in manifest:
            cp(os.path.join(prev, file_), file_, create_dirs=True)

        bmi = Bmi()
        bmi.initialize(infile)

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
    params = get_test_parameters()

    if "gid" in metafunc.fixturenames:
        metafunc.parametrize("gid", params["gid"])
    elif "var_name" in metafunc.fixturenames:
        metafunc.parametrize("var_name", params["var_name"])
    elif "in_var_name" in metafunc.fixturenames:
        metafunc.parametrize("in_var_name", params["in_var_name"])
    elif "out_var_name" in metafunc.fixturenames:
        metafunc.parametrize("out_var_name", params["out_var_name"])

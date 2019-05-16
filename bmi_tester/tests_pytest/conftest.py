from __future__ import print_function

import importlib
import os

import pytest

from scripting import cd, cp


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


try:
    class_to_test = os.environ["BMITEST_CLASS"]
except KeyError:
    Bmi = None
else:
    Bmi = load_component(class_to_test)
INPUT_FILE = os.environ.get("BMITEST_INPUT_FILE", None)
BMI_VERSION_STRING = os.environ.get("BMI_VERSION_STRING", "1.1")


def all_grids(bmi, gtype=None):
    in_names = set(bmi.get_input_var_names())
    out_names = set(bmi.get_output_var_names())

    grids = set()
    for name in in_names | out_names:
        gid = bmi.get_var_grid(name)
        if gtype == bmi.get_grid_type(gid)[1] or gtype is None:
            grids.add(gid)
    return grids


def get_test_parameters(infile=None):
    infile = infile or INPUT_FILE

    try:
        with open(".ROOT_DIR", "r") as fp:
            root_dir = fp.read()
    except IOError:
        root_dir = "."

    bmi = Bmi()
    with cd(root_dir):
        bmi.initialize(infile or INPUT_FILE)

    in_names = set(bmi.get_input_var_names())
    out_names = set(bmi.get_output_var_names())

    meta = {
        "gid": all_grids(bmi),
        "var_name": in_names | out_names,
        "in_var_name": in_names - out_names,
        "out_var_name": out_names,
    }

    return meta


@pytest.fixture(scope="session")
def bmi():
    return Bmi()


@pytest.fixture(scope="session")
def initialized_bmi(tmpdir_factory, infile=None, manifest=None):
    infile = os.environ.get("BMITEST_INPUT_FILE", None)
    manifest = os.environ.get("BMITEST_MANIFEST", infile or "").splitlines()

    tmp = tmpdir_factory.mktemp("data")
    with tmp.as_cwd() as prev:
        for file_ in [fname.strip() for fname in manifest]:
            if file_:
                cp(os.path.join(str(prev), file_), file_, create_dirs=True)

        bmi = Bmi()
        bmi.initialize(infile)

    return bmi


@pytest.fixture
def staged_tmpdir(tmpdir, infile=None, manifest=None):
    infile = os.environ.get("BMITEST_INPUT_FILE", None)
    manifest = os.environ.get("BMITEST_MANIFEST", infile or "").splitlines()
    with tmpdir.as_cwd() as prev:
        for file_ in [fname.strip() for fname in manifest]:
            if file_:
                cp(os.path.join(str(prev), file_), file_, create_dirs=True)
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

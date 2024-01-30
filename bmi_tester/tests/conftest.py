import contextlib
import importlib
import os
import shutil
from collections.abc import Generator

import pytest
from packaging.version import Version


@contextlib.contextmanager
def as_cwd(path: str) -> Generator[None, None, None]:
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_cwd)


def skip_if_grid_type_is_not(bmi, gid, gtype):
    if isinstance(gtype, str):
        gtype = (gtype,)
    if bmi.get_grid_type(gid) not in gtype:
        gtypes = ", ".join(gtype)
        if len(gtype) > 1:
            pytest.skip(f"grid {gid} is not one of {gtypes}")
        else:
            pytest.skip(f"grid {gid} is not {gtypes}")


def skip_if_grid_type_is(bmi, gid, gtype):
    if isinstance(gtype, str):
        gtype = (gtype,)
    if bmi.get_grid_type(gid) in gtype:
        gtypes = ", ".join(gtype)
        if len(gtype) > 1:
            pytest.skip(f"grid {gid} is one of {gtypes}")
        else:
            pytest.skip(f"grid {gid} is {gtypes}")


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
INPUT_FILE = os.environ.get("BMITEST_INPUT_FILE")
# BMI_VERSION_STRING = os.environ.get("BMI_VERSION_STRING", "1.1")
BMI_VERSION_STRING = os.environ.get("BMI_VERSION_STRING", "2.0")
BMI_VERSION = Version(BMI_VERSION_STRING)


def all_grids(bmi, gtype=None):
    in_names = set(bmi.get_input_var_names())
    out_names = set(bmi.get_output_var_names())

    grids = set()
    for name in in_names | out_names:
        if bmi.get_var_location(name) != "none":
            gid = bmi.get_var_grid(name)
            if gtype == bmi.get_grid_type(gid)[1] or gtype is None:
                grids.add(gid)
    return grids


count = 1


def get_test_parameters(infile=None, count=0):
    infile = infile or INPUT_FILE

    try:
        with open(".ROOT_DIR") as fp:
            root_dir = fp.read()
    except OSError:
        root_dir = "."
    if count > 1:
        raise RuntimeError()
    count += 1

    bmi = Bmi()
    with as_cwd(root_dir):
        bmi.initialize(infile)

        in_names = set(bmi.get_input_var_names())
        out_names = set(bmi.get_output_var_names())
        grids = set(all_grids(bmi))

        # in_names = set()
        # out_names = set()
        # grids = set()

        bmi.finalize()

    meta = {
        "gid": grids,
        "var_name": in_names | out_names,
        "in_var_name": in_names - out_names,
        "out_var_name": out_names,
    }

    return meta


@pytest.fixture(scope="session")
def bmi():
    # return None
    return Bmi()


@pytest.fixture(scope="session")
def initialized_bmi(tmpdir_factory, infile=None, manifest=None):
    infile = os.environ.get("BMITEST_INPUT_FILE")
    manifest = os.environ.get("BMITEST_MANIFEST", infile or "").splitlines()

    tmp = tmpdir_factory.mktemp("data")
    with tmp.as_cwd() as prev:
        for file_ in [fname.strip() for fname in manifest]:
            if file_:
                os.makedirs(tmp / os.path.dirname(file_), exist_ok=True)
                shutil.copy2(prev / file_, tmp / file_)

        bmi = Bmi()
        bmi.initialize(infile)
    # return None
    return bmi


@pytest.fixture(scope="function")
def staged_tmpdir(tmpdir, infile=None, manifest=None):
    infile = os.environ.get("BMITEST_INPUT_FILE")
    manifest = os.environ.get("BMITEST_MANIFEST", infile or "").splitlines()
    with tmpdir.as_cwd() as prev:
        for file_ in [fname.strip() for fname in manifest]:
            if file_:
                os.makedirs(tmpdir / os.path.dirname(file_), exist_ok=True)
                shutil.copy2(prev / file_, tmpdir / file_)
    return tmpdir


params = get_test_parameters(count=count)


@pytest.fixture(scope="session", params=params["out_var_name"])
def out_var_name(request):
    param = request.param
    return param


@pytest.fixture(scope="session", params=params["var_name"])
def var_name(request):
    param = request.param
    return param


def pytest_generate_tests(metafunc):
    if "gid" in metafunc.fixturenames:
        metafunc.parametrize("gid", params["gid"])
    # elif "var_name" in metafunc.fixturenames:
    #     metafunc.parametrize("var_name", params["var_name"])
    elif "in_var_name" in metafunc.fixturenames:
        metafunc.parametrize("in_var_name", params["in_var_name"])
    # elif "out_var_name" in metafunc.fixturenames:
    #     metafunc.parametrize("out_var_name", params["out_var_name"])

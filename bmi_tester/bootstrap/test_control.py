import importlib
import os

import pytest
from scripting import cp


# from .conftest import INPUT_FILE, Bmi

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


@pytest.mark.dependency()
def test_has_initialize():
    """Test component has an initialize method."""
    bmi = Bmi()
    assert hasattr(bmi, "initialize")


@pytest.mark.dependency()
def test_has_finalize():
    """Test component has a finalize method."""
    bmi = Bmi()
    assert hasattr(bmi, "finalize")


@pytest.mark.dependency(depends=["has_initialize", "has_finalize"], name="initialize_works")
def test_initialize(tmpdir):
    """Test component can initialize itself."""
    infile = os.environ.get("BMITEST_INPUT_FILE", None)
    manifest = os.environ.get("BMITEST_MANIFEST", infile or "").splitlines()

    with tmpdir.as_cwd() as prev:
        for file_ in [fname.strip() for fname in manifest]:
            if file_:
                cp(os.path.join(str(prev), file_), tmpdir / file_, create_dirs=True)

        bmi = Bmi()
        assert bmi.initialize(INPUT_FILE) is None
        bmi.finalize()


@pytest.mark.dependency(depends=["initialize_works"])
def test_update(tmpdir):
    """Test component can update itself."""
    infile = os.environ.get("BMITEST_INPUT_FILE", None)
    manifest = os.environ.get("BMITEST_MANIFEST", infile or "").splitlines()

    with tmpdir.as_cwd() as prev:
        for file_ in [fname.strip() for fname in manifest]:
            if file_:
                cp(os.path.join(str(prev), file_), tmpdir / file_, create_dirs=True)

        bmi = Bmi()
        bmi.initialize(INPUT_FILE)
        assert bmi.update() is None
        bmi.finalize()

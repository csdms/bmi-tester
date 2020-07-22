import pytest

from .conftest import INPUT_FILE, Bmi


def test_has_initialize(bmi):
    """Test component has an initialize method."""
    assert hasattr(bmi, "initialize")


@pytest.mark.dependency(name="initialize_works")
def test_initialize(staged_tmpdir):
    """Test component can initialize itself."""
    with staged_tmpdir.as_cwd():
        bmi = Bmi()
        assert bmi.initialize(INPUT_FILE) is None
        bmi.finalize()


@pytest.mark.dependency(depends=["initialize_works"])
def test_update(staged_tmpdir):
    """Test component can update itself."""
    with staged_tmpdir.as_cwd():
        bmi = Bmi()
        bmi.initialize(INPUT_FILE)
        assert bmi.update() is None
        bmi.finalize()


def test_has_finalize(bmi):
    """Test component has a finalize method."""
    assert hasattr(bmi, "finalize")

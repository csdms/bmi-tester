import contextlib

import pytest


@pytest.mark.dependency()
def test_has_initialize(bmi_factory):
    """Test component has an initialize method."""
    model = bmi_factory()
    assert hasattr(model, "initialize")
    assert callable(model.initialize)


@pytest.mark.dependency()
def test_has_finalize(bmi_factory):
    """Test component has a finalize method."""
    model = bmi_factory()
    assert hasattr(model, "finalize")
    assert callable(model.finalize)


@pytest.mark.dependency()
def test_has_update(bmi_factory):
    """Test component has an update method."""
    model = bmi_factory()
    assert hasattr(model, "update")
    assert callable(model.update)


@pytest.mark.dependency(
    depends=(
        "test_has_initialize",
        "test_has_finalize",
    ),
    name="initialize_works",
)
def test_initialize(staged_tmpdir, bmi_factory, bmi_config):
    """Test component can initialize itself."""
    with staged_tmpdir.as_cwd():
        model = bmi_factory()
        result = model.initialize(bmi_config.input_file)
        try:
            assert result is None
        finally:
            model.finalize()


@pytest.mark.dependency(
    depends=(
        "test_has_initialize",
        "test_has_finalize",
    ),
    name="finalize_works",
)
def test_finalize(staged_tmpdir, bmi_factory, bmi_config):
    """Test component can finalize itself."""
    with staged_tmpdir.as_cwd():
        model = bmi_factory()
        model.initialize(bmi_config.input_file)

        result = model.finalize()
        assert result is None


@pytest.mark.dependency(
    depends=(
        "initialize_works",
        "test_has_update",
    )
)
def test_update(staged_tmpdir, bmi_factory, bmi_config):
    """Test component can update itself."""
    with staged_tmpdir.as_cwd():
        model = bmi_factory()
        model.initialize(bmi_config.input_file)
        with contextlib.suppress(NotImplementedError):
            assert model.update() is None
        model.finalize()

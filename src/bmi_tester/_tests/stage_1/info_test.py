import warnings

import pytest
from packaging.version import Version
from standard_names.standardname import StandardName
from standard_names.standardname import is_valid_name


def test_get_component_name(initialized_bmi):
    """Test component name is a string."""
    name = initialized_bmi.get_component_name()
    assert isinstance(name, str)


def test_var_names(var_name):
    """Test var names are valid."""
    assert isinstance(var_name, str)
    if is_valid_name(var_name):
        StandardName(var_name)
    else:
        warnings.warn(f"not a valid standard name: {var_name}", stacklevel=2)


@pytest.mark.dependency()
def test_input_var_name_count(initialized_bmi, bmi_version):
    if bmi_version < Version("2.0"):
        func_name = "get_input_var_name_count"
    else:
        func_name = "get_input_item_count"

    if hasattr(initialized_bmi, func_name):
        n_names = getattr(initialized_bmi, func_name)()
        assert isinstance(n_names, int)
        assert n_names >= 0
    else:
        pytest.skip(f"{func_name} not implemented")


@pytest.mark.dependency()
def test_output_var_name_count(initialized_bmi, bmi_version):
    if bmi_version < Version("2.0"):
        func_name = "get_output_var_name_count"
    else:
        func_name = "get_output_item_count"

    if hasattr(initialized_bmi, func_name):
        n_names = getattr(initialized_bmi, func_name)()
        assert isinstance(n_names, int)
        assert n_names >= 0
    else:
        pytest.skip(f"{func_name} not implemented")


def test_get_input_var_names(initialized_bmi, bmi_version):
    """Input var names is a tuple of strings."""
    func_name = "item" if bmi_version >= Version("2.0") else "var_name"

    get_count = getattr(initialized_bmi, f"get_input_{func_name}_count", None)

    assert hasattr(initialized_bmi, "get_input_var_names")
    names = initialized_bmi.get_input_var_names()

    assert isinstance(names, tuple)
    assert all(isinstance(name, str) for name in names)

    if get_count is not None:
        n_names = get_count()
        assert len(names) == n_names
    else:
        warnings.warn(f"get_input_{func_name}_count not implemented", stacklevel=2)


def test_get_output_var_names(initialized_bmi, bmi_version):
    """Output var names is a tuple of strings."""
    func_name = "item" if bmi_version >= Version("2.0") else "var_name"

    get_count = getattr(initialized_bmi, f"get_output_{func_name}_count", None)

    assert hasattr(initialized_bmi, "get_output_var_names")
    names = initialized_bmi.get_output_var_names()

    assert isinstance(names, tuple)
    assert all(isinstance(name, str) for name in names)

    if get_count is not None:
        n_names = get_count()
        assert len(names) == n_names
    else:
        warnings.warn(f"get_output_{func_name}_count not implemented", stacklevel=2)

#! /usr/bin/env python
import warnings

import pytest

import standard_names


def test_get_component_name(initialized_bmi):
    """Test component name is a string."""
    name = initialized_bmi.get_component_name()
    assert isinstance(name, str)

    return name


def test_var_names(var_name):
    """Test var names are valid."""
    assert isinstance(var_name, str)
    if standard_names.is_valid_name(var_name):
        standard_names.StandardName(var_name)
    else:
        warnings.warn("not a valid standard name: {name}".format(name=var_name))


def test_input_var_name_count(initialized_bmi):
    if hasattr(initialized_bmi, "get_input_var_name_count"):
        n_names = initialized_bmi.get_input_var_name_count()
        assert isinstance(n_names, int)
        assert n_names >= 0
    else:
        pytest.skip("get_input_var_name_count not implemented")


def test_output_var_name_count(initialized_bmi):
    if hasattr(initialized_bmi, "get_output_var_name_count"):
        n_names = initialized_bmi.get_output_var_name_count()
        assert isinstance(n_names, int)
        assert n_names >= 0
    else:
        pytest.skip("get_output_var_name_count not implemented")


def test_get_input_var_names(initialized_bmi):
    """Input var names is a list of strings."""
    names = initialized_bmi.get_input_var_names()
    assert isinstance(names, tuple)

    if hasattr(initialized_bmi, "get_input_var_name_count"):
        n_names = initialized_bmi.get_input_var_name_count()
        assert len(names) == n_names
    else:
        warnings.warn("get_input_var_name_count not implemented")


def test_get_output_var_names(initialized_bmi):
    """Output var names is a list of strings."""
    names = initialized_bmi.get_output_var_names()
    assert isinstance(names, tuple)

    if hasattr(initialized_bmi, "get_output_var_name_count"):
        n_names = initialized_bmi.get_output_var_name_count()
        assert len(names) == n_names
    else:
        warnings.warn("get_output_var_name_count not implemented")

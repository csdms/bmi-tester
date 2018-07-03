#! /usr/bin/env python
from nose.tools import assert_is_instance
from nose import with_setup

import standard_names

from .utils import setup_func, teardown_func, all_names, new_bmi


@with_setup(setup_func, teardown_func)
def test_get_component_name():
    """Test component name is a string."""
    name = new_bmi().get_component_name()
    assert_is_instance(name, str)

    return name


@with_setup(setup_func, teardown_func)
def test_var_names():
    """Test var names are valid."""
    bmi = new_bmi()
    for name in all_names(bmi):

        def _check_is_str(name):
            assert_is_instance(name, str)

        def _check_is_valid(name):
            standard_names.StandardName(name)

        _check_is_str.description = "Test {name} is str".format(name=name)
        _check_is_valid.description = "Test {name} is a Standard Name".format(name=name)
        yield _check_is_str, name
        yield _check_is_valid, name


@with_setup(setup_func, teardown_func)
def test_get_input_var_names():
    """Input var names is a list of strings."""
    names = new_bmi().get_input_var_names()
    assert_is_instance(names, tuple)


@with_setup(setup_func, teardown_func)
def test_get_output_var_names():
    """Output var names is a list of strings."""
    names = new_bmi().get_output_var_names()
    assert_is_instance(names, tuple)

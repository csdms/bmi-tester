#! /usr/bin/env python
from nose.tools import assert_true
from nose import with_setup

from . import Bmi, INPUT_FILE
from .utils import setup_func, teardown_func, new_bmi


@with_setup(setup_func, teardown_func)
def test_has_initialize():
    """Test component has an initialize method."""
    assert_true(hasattr(new_bmi(), "initialize"))


# @with_setup(setup_func, teardown_func)
def test_initialize():
    """Test component can initialize itself."""
    bmi = Bmi()
    bmi.initialize(INPUT_FILE)


@with_setup(setup_func, teardown_func)
def test_has_finalize():
    """Test component has a finalize method."""
    assert_true(hasattr(new_bmi(), "finalize"))

#! /usr/bin/env python
from nose.tools import (assert_is_instance, assert_greater_equal,
                        assert_less_equal, assert_almost_equal,
                        assert_true)
from nose import with_setup

import cfunits

from .utils import setup_func, teardown_func, new_bmi


@with_setup(setup_func, teardown_func)
def test_get_start_time():
    """Test that there is a start time."""
    bmi = new_bmi()
    start = bmi.get_start_time()
    time_step = bmi.get_time_step()

    assert_is_instance(start, float)
    assert_almost_equal(start, 0.)


@with_setup(setup_func, teardown_func)
def test_get_time_step():
    """Test that there is a time step."""
    time_step = new_bmi().get_time_step()
    assert_is_instance(time_step, float)


@with_setup(setup_func, teardown_func)
def test_time_units_is_str():
    """Test the units of time is a str."""
    units = new_bmi().get_time_units()
    assert_is_instance(units, str)


@with_setup(setup_func, teardown_func)
def test_time_units_is_valid():
    """Test the units of time are valid."""
    units = cfunits.Units(new_bmi().get_time_units())
    assert_true(units.istime)


@with_setup(setup_func, teardown_func)
def test_get_current_time():
    """Test that there is a current time."""
    bmi = new_bmi()
    start = bmi.get_start_time()
    now = bmi.get_current_time()
    stop = bmi.get_end_time()

    assert_is_instance(now, (int, float))
    assert_less_equal(now, stop)
    assert_greater_equal(now , start)


@with_setup(setup_func, teardown_func)
def test_get_end_time():
    """Test that there is a stop time."""
    bmi = new_bmi()
    start = bmi.get_start_time()
    stop = bmi.get_end_time()

    assert_is_instance(stop, (int, float))
    assert_greater_equal(stop, start)

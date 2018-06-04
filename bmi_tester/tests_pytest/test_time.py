#! /usr/bin/env python
from nose.tools import assert_almost_equal

import cfunits


def test_get_start_time(new_bmi):
    """Test that there is a start time."""
    start = new_bmi.get_start_time()

    assert isinstance(start, float)
    assert_almost_equal(start, 0.)


def test_get_time_step(new_bmi):
    """Test that there is a time step."""
    time_step = new_bmi.get_time_step()

    assert isinstance(time_step, float)


def test_time_units_is_str(new_bmi):
    """Test the units of time is a str."""
    units = new_bmi.get_time_units()

    assert isinstance(units, str)


def test_time_units_is_valid(new_bmi):
    """Test the units of time are valid."""
    units = new_bmi.get_time_units()
    units = cfunits.Units(units)

    assert units.istime


def test_get_current_time(new_bmi):
    """Test that there is a current time."""
    start = new_bmi.get_start_time()
    now = new_bmi.get_current_time()
    stop = new_bmi.get_end_time()

    assert isinstance(now, (int, float))
    assert now <= stop
    assert now >= start


def test_get_end_time(new_bmi):
    """Test that there is a stop time."""
    start = new_bmi.get_start_time()
    stop = new_bmi.get_end_time()

    assert isinstance(stop, (int, float))
    assert stop >= start

#! /usr/bin/env python
# try:
#     from pymt import cfunits
# except (FileNotFoundError, ModuleNotFoundError):
#     cfunits = None
import pytest
from pytest import approx

from bmi_tester.units import Units


@pytest.mark.dependency()
def test_get_start_time(initialized_bmi):
    """Test that there is a start time."""
    start = initialized_bmi.get_start_time()

    assert isinstance(start, float)
    assert start == approx(0.0)


@pytest.mark.dependency()
def test_get_time_step(initialized_bmi):
    """Test that there is a time step."""
    time_step = initialized_bmi.get_time_step()

    assert isinstance(time_step, float)


def test_time_units_is_str(initialized_bmi):
    """Test the units of time is a str."""
    units = initialized_bmi.get_time_units()

    assert isinstance(units, str)


# @pytest.mark.skipif(cfunits is None, reason="cfunits is broken on this platform")
def test_time_units_is_valid(initialized_bmi):
    """Test the units of time are valid."""
    units = initialized_bmi.get_time_units()
    unit_system = Units()
    assert unit_system.is_valid(units)
    assert unit_system.is_time(units)
    # units = cfunits.Units(units)
    # assert units.istime


@pytest.mark.dependency(depends=["test_get_start_time", "test_get_end_time"])
def test_get_current_time(initialized_bmi):
    """Test that there is a current time."""
    start = initialized_bmi.get_start_time()
    now = initialized_bmi.get_current_time()
    stop = initialized_bmi.get_end_time()

    assert isinstance(now, (int, float))
    assert now <= stop
    assert now >= start


@pytest.mark.skip()
@pytest.mark.dependency(depends=["test_get_start_time"])
def test_get_end_time(initialized_bmi):
    """Test that there is a stop time."""
    start = initialized_bmi.get_start_time()
    stop = initialized_bmi.get_end_time()

    assert isinstance(stop, (int, float))
    assert stop >= start

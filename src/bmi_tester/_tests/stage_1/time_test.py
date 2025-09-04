#! /usr/bin/env python
# try:
#     from pymt import cfunits
# except (FileNotFoundError, ModuleNotFoundError):
#     cfunits = None
import pytest
from pytest import approx

from bmi_tester.api import WITH_GIMLI_UNITS
from bmi_tester.api import check_unit_is_dimensionless
from bmi_tester.api import check_unit_is_time
from bmi_tester.api import check_unit_is_valid


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


@pytest.mark.skipif(not WITH_GIMLI_UNITS, reason="gimli.units is not installed")
def test_time_units_is_valid(initialized_bmi):
    """Test the units of time are valid."""
    units = initialized_bmi.get_time_units()
    assert check_unit_is_valid(units)
    assert check_unit_is_time(units) or check_unit_is_dimensionless(units)


@pytest.mark.dependency(depends=["test_get_start_time", "test_get_end_time"])
def test_get_current_time(initialized_bmi):
    """Test that there is a current time."""
    start = initialized_bmi.get_start_time()
    now = initialized_bmi.get_current_time()
    stop = initialized_bmi.get_end_time()
    time_step = initialized_bmi.get_time_step()

    assert isinstance(now, (int, float))

    # Test that the current time is 'between' the start and stop
    # times; this depends on whether the time step is negative, positive, or 0
    assert (((time_step > 0) & (now <= stop))
            # Inverse model has current time greater than the stop
           | ((time_step < 0) & (now >= stop))
           # Instantaneous model has current time equal stop
           | ((time_step == 0) & (now == stop)))
    assert (((time_step > 0) & (now >= start))
            # Inverse model has current time less than the start
            | ((time_step < 0) & (now <= start))
            # Instantaneous model has current time equalt the start
            | ((time_step == 0) & (now == start)))

@pytest.mark.skip()
@pytest.mark.dependency(depends=["test_get_start_time"])
def test_get_end_time(initialized_bmi):
    """Test that there is a stop time."""
    start = initialized_bmi.get_start_time()
    stop = initialized_bmi.get_end_time()
    time_step = initialized_bmi.get_time_step()

    assert isinstance(stop, (int, float))
    assert ((time_step > 0 & start <= stop)
          # or an inverse model
         | (time_step < 0 & stop <= start)
          # or an instantaneous model
         | (time_step == 0 & start == stop))

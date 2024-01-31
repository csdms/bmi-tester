import pytest

from bmi_tester.api import check_unit_is_dimensionless
from bmi_tester.api import check_unit_is_time
from bmi_tester.api import check_unit_is_valid


@pytest.mark.parametrize(
    "unit", ("m", "m / s", "m s-1", "N m", "N.m", "m^2", "m2", "", "1")
)
def test_check_valid_units(unit):
    assert check_unit_is_valid(unit)


@pytest.mark.parametrize("unit", ("foo", "m ** 2", "-"))
def test_check_invalid_units(unit):
    assert not check_unit_is_valid(unit)


@pytest.mark.parametrize("unit", ("", "1"))
def test_dimensionless_units(unit):
    assert check_unit_is_dimensionless(unit)


def test_not_dimensionless_units():
    assert not check_unit_is_dimensionless("m")


@pytest.mark.parametrize(
    "unit",
    (
        "s",
        "d",
        "yr",
        "seconds since 1970-01-01",
        "seconds since 1970-01-01 00:00:00 UTC",
        "days since 1970-01-01 00:00:00 UTC",
        "years since 1970-01-01 00:00:00 UTC",
    ),
)
def test_time_units(unit):
    assert check_unit_is_time(unit)


def test_not_time_units():
    assert not check_unit_is_time("m")

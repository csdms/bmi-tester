from bmi_tester.api import check_unit_is_dimensionless
from bmi_tester.api import check_unit_is_time
from bmi_tester.api import check_unit_is_valid


def test_check_valid_units():
    assert check_unit_is_valid("m")
    assert check_unit_is_valid("m / s")
    assert check_unit_is_valid("m s-1")
    assert check_unit_is_valid("N m")
    assert check_unit_is_valid("N.m")
    assert check_unit_is_valid("m^2")
    assert check_unit_is_valid("m2")
    assert check_unit_is_valid("")
    assert check_unit_is_valid("1")


def test_check_invalid_units():
    assert not check_unit_is_valid("foo")
    assert not check_unit_is_valid("m ** 2")
    assert not check_unit_is_valid("-")


def test_dimensionless_units():
    assert check_unit_is_dimensionless("")
    assert check_unit_is_dimensionless("1")
    assert not check_unit_is_dimensionless("m")
    # assert not check_unit_is_dimensionless("-")


def test_time_units():
    assert check_unit_is_time("s")
    assert check_unit_is_time("d")
    assert check_unit_is_time("yr")
    assert check_unit_is_time("seconds since 1970-01-01")
    assert check_unit_is_time("seconds since 1970-01-01 00:00:00 UTC")
    assert check_unit_is_time("days since 1970-01-01 00:00:00 UTC")
    assert check_unit_is_time("years since 1970-01-01 00:00:00 UTC")

    assert not check_unit_is_time("m")

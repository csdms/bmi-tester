from bmi_tester.units import Units


def test_check_valid_units():
    unit_system = Units()
    assert unit_system.is_valid("m")
    assert unit_system.is_valid("m / s")
    assert unit_system.is_valid("m s-1")
    assert unit_system.is_valid("N m")
    assert unit_system.is_valid("N.m")
    assert unit_system.is_valid("m^2")
    assert unit_system.is_valid("m2")
    assert unit_system.is_valid("")
    assert unit_system.is_valid("1")


def test_check_invalid_units():
    unit_system = Units()
    assert not unit_system.is_valid("foo")
    assert not unit_system.is_valid("m ** 2")
    assert not unit_system.is_valid("-")

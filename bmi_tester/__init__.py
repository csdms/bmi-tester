from importlib.metadata import version

from .api import (
    check_bmi,
    check_unit_is_dimensionless,
    check_unit_is_time,
    check_unit_is_valid,
)

__version__ = version("bmi_tester")
__all__ = [
    "check_bmi",
    "check_unit_is_valid",
    "check_unit_is_time",
    "check_unit_is_dimensionless",
]

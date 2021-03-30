import pkg_resources

from .api import check_bmi, check_unit_is_valid, check_unit_is_time, check_unit_is_dimensionless

__version__ = pkg_resources.get_distribution("bmi_tester").version
__all__ = [
    "check_bmi",
    "check_unit_is_valid",
    "check_unit_is_time",
    "check_unit_is_dimensionless",
]
del pkg_resources

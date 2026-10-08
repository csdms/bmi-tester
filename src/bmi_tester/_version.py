from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    __version__ = version("bmi_tester")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

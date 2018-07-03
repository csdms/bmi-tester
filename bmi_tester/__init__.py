from .bmitester import BmiTester
from .api import run_test


__all__ = ['BmiTester', 'run_test']

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from __future__ import print_function

import os
import traceback

import numpy as np
from nose import with_setup
from nose.tools import nottest
from nose.tools import (assert_is_instance, assert_greater_equal,
                        assert_less_equal, assert_almost_equal,
                        assert_greater, assert_in)

from .termcolors import red, green, yellow, blink

# from components import InfilGreenAmpt as Component


# _INPUT_FILE = 'input/infil_green_ampt.cfg'


_ERROR_MESSAGE = """
------------------------------------------------------------------------------
{name}:

{traceback}
------------------------------------------------------------------------------
"""


_RESULT_TO_STRING = {
    0: green('PASS'),
    1: red('FAIL'),
    2: blink(red('ERROR')),
}


def print_status(msg):
    print(msg + '... ', end='')


def print_result(result, msg=None):
    msg = msg or _RESULT_TO_STRING[result]

    if result is True or result == 0:
        print(green(msg))
    else:
        print(red(msg))


class FuncTester(object):
    def __init__(self, context):
        self._context = context
        self._n_errors = 0

    def run(self):
        self._context._result = self._context._func()


class testing(object):
    def __init__(self, func, verbose=True):
        self._func = func
        self._msg = func.__doc__ or func.__name__
        self._result = None
        self._verbose = verbose

    def __enter__(self):
        print_status(self._msg)
        return FuncTester(self)

    def __exit__(self, type, value, exc_tb):
        if type is None:
            result = 0
            msg = self._result
        else:
            if self._verbose:
                msg = traceback.format_exc()
            else:
                msg = traceback.format_exc().strip().splitlines()[-1]
            if isinstance(type, AssertionError):
                result = 1
            else:
                result = 2
        print_result(result, msg=msg)
        return True


class Tester(object):
    def __init__(self):
        self._results = {}

    @property
    def results(self):
        return tuple(self._results.items())

    def find_tests(self):
        import inspect
        tests = {}
        for name, func in inspect.getmembers(self):
            if name.startswith('test_'):
                tests[name] = func
        return tests

    def _record_error(self, test_name, desc, result, msg=None):
        err_message = self._format_error(test_name)
        if result == 1:
            result_str = 'fail'
        else:
            result_str = 'error'

        self._results[test_name] = {
            'result': result_str,
            'desc': desc,
            'message': err_message,
        }

    def _record_pass(self, test_name, desc, msg=None):
        self._results[test_name] = {
            'result': 'pass',
            'desc': desc,
            'message': msg or 'none',
        }

    def _record_result(self, test_name, desc, result, msg=None):
        if result == 0:
            self._record_pass(test_name, desc, msg)
        else:
            self._record_error(test_name, desc, msg)

    def _format_error(self, test_name):
        return _ERROR_MESSAGE.format(
            name=test_name, traceback=traceback.format_exc())

    def run_test_func(self, func):
        with testing(func, verbose=False) as test:
            test.run()
        return 0

    def foreach(self, args, func):
        print()
        n_fails = 0
        for arg in args:
            def _test():
                return func(arg)
            _test.__doc__ = """  Test {arg}""".format(arg=arg)
            _test.__name__ = "test_{name}".format(name=arg)

            n_fails += self.run_test_func(_test)

        if n_fails > 0:
            raise AssertionError('There were some problems.')

    def run(self):
        for name, func in self.find_tests().items():
            self.run_test_func(func)
        self.print_summary()

    def print_summary(self):
        n_fails = 0
        for name, test in self._results.items():
            if test['result'] == 'fail':
                print('{error}'.format(error=test['message']))
                n_fails += 1

        n_errors = 0
        for name, test in self._results.items():
            if test['result'] == 'error':
                print('{error}'.format(error=test['message']))
                n_errors += 1

        print('errors={n_errors}, failures={n_fails}'.format(
            n_errors=n_errors, n_fails=n_fails))


class BmiTester(Tester):
    def __init__(self, bmi, file=None):
        self._bmi = bmi
        self._file = file

        self.bmi.initialize(file)
        # self.bmi.update()

        super(BmiTester, self).__init__()

    @property
    def bmi(self):
        return self._bmi

    def test_get_component_name(self):
        """Test component has a name."""
        name = self.bmi.get_component_name()
        assert_is_instance(name, str)
        return name

    def test_initialize(self):
        """Test initialization from a file."""
        self.bmi.initialize(self._file)

    def test_get_input_var_names(self):
        """Input var names is a list of strings."""
        names = self.bmi.get_input_var_names()
        assert_is_instance(names, tuple)
        for name in names:
            assert_is_instance(name, str)
        return '{count} input vars'.format(count=len(names))

    def test_get_output_var_names(self):
        """Input var names is a list of strings."""
        names = self.bmi.get_output_var_names()
        assert_is_instance(names, tuple)
        for name in names:
            assert_is_instance(name, str)
        return '{count} output vars'.format(count=len(names))

    def test_get_input_values(self):
        """Input values are numpy arrays."""
        n_fails = 0
        names = self.bmi.get_input_var_names()
        print()
        for name in names:
            def _test():
                val = self.bmi.get_value(name)
                assert_is_instance(val, np.ndarray)
                return 'ndarray of {dtype}, shape {shape}'.format(dtype=val.dtype, shape=val.shape)
            _test.__doc__ = """  Test get_value for {name}""".format(name=name)
            _test.__name__ = 'test_{name}'.format(name=name)

            n_fails += self.run_test_func(_test)

        if n_fails > 0:
            raise AssertionError('There were some problems with input values')

    def test_get_output_values(self):
        """Output values are numpy arrays."""
        n_fails = 0
        names = self.bmi.get_output_var_names()
        print()
        for name in names:
            def _test():
                val = self.bmi.get_value(name)
                assert_is_instance(val, np.ndarray)
                return 'ndarray of {dtype}, shape {shape}'.format(dtype=val.dtype, shape=val.shape)
            _test.__doc__ = """  Test get_value for {name}""".format(name=name)
            _test.__name__ = 'test_{name}'.format(name=name)

            n_fails += self.run_test_func(_test)

        if n_fails > 0:
            raise AssertionError('There were some problems with output values')

    def test_get_time_step(self):
        """Test that there is a time step."""
        time_step = self.bmi.get_time_step()
        assert_is_instance(time_step, float)
        return str(time_step)

    def test_get_start_time(self):
        """Test that there is a start time."""
        start = self.bmi.get_start_time()
        time_step = self.bmi.get_time_step()

        assert_is_instance(start, float)
        assert_almost_equal(start, 0.)
        return str(start)

    def test_get_end_time(self):
        """Test that there is a stop time."""
        start = self.bmi.get_start_time()
        stop = self.bmi.get_end_time()

        assert_is_instance(stop, float)
        assert_greater_equal(stop, start)
        return str(stop)

    def test_get_current_time(self):
        """Test that there is a current time."""
        start = self.bmi.get_start_time()
        now = self.bmi.get_current_time()
        stop = self.bmi.get_end_time()

        assert_is_instance(now, float)
        assert_less_equal(now, stop)
        assert_greater_equal(now , start)
        return str(now)

    def test_get_time_units(self):
        """Test the units of time."""
        units = self.bmi.get_time_units()
        assert_in(units, ('s', 'seconds', 'd', 'days', 'y', 'years'))
        return units

    def _test_var_rank(self, name):
        """Test var rank."""
        rank = self.bmi.get_var_rank(name)
        assert_is_instance(rank, int)
        return str(rank)

    def _test_var_units(self, name):
        """Test var units."""
        units = self.bmi.get_var_units(name)
        assert_is_instance(units, str)
        assert_greater(len(units), 0)
        return units

    def _test_var_grid(self, name):
        """Test var grids."""
        grid = self.bmi.get_var_grid(name)
        assert_is_instance(grid, int)
        return str(grid)

    def test_get_var_rank(self):
        """Test the rank of the variables."""
        names = set(self.bmi.get_input_var_names()) | set(self.bmi.get_output_var_names())
        self.foreach(names, self._test_var_rank)

    def test_get_var_units(self):
        """Test the units of the variables."""
        names = set(self.bmi.get_input_var_names()) | set(self.bmi.get_output_var_names())
        self.foreach(names, self._test_var_units)

    def test_get_var_grid(self):
        """Test the grid of the variables."""
        names = set(self.bmi.get_input_var_names()) | set(self.bmi.get_output_var_names())
        self.foreach(names, self._test_var_grid)

    def _test_grid_type(self, grid):
        """Test the type of a grid."""
        type_str = self.bmi.get_grid_type(grid)
        assert_is_instance(type_str, str)
        assert_in(type_str, ("scalar", "vector", "uniform_rectilinear"))
        return type_str

    def _test_grid_shape(self, grid):
        """Test grid shape."""
        if self.bmi.get_grid_type(grid) == 'uniform_rectilinear':
            shape = self.bmi.get_grid_shape(grid)
            assert_is_instance(shape, tuple)
            ndim = len(shape)
            assert_greater_equal(ndim, 1)
            assert_less_equal(ndim, 2)
            for dim in shape:
                assert_is_instance(dim, int)
            return str(shape)
        return 'no shape'

    def test_get_grid_type(self):
        """Test the grid type."""
        grids = []
        for name in set(self.bmi.get_input_var_names()) | set(self.bmi.get_output_var_names()):
            grids.append( self.bmi.get_var_grid(name) )
        self.foreach(grids, self._test_grid_type)

    def test_get_grid_shape(self):
        """Test the grid shape."""
        grids = []
        for name in set(self.bmi.get_input_var_names()) | set(self.bmi.get_output_var_names()):
            grids.append( self.bmi.get_var_grid(name) )
        self.foreach(grids, self._test_grid_shape)

if __name__ == '__main__':
    tester = BmiTester(Component(), file=_INPUT_FILE)
    tester.run()

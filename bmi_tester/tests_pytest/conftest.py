import os

import pytest
from scripting.contexts import cd

from . import Bmi, INPUT_FILE
from .utils import all_grids, all_names, out_names, strictly_input_names


@pytest.fixture(scope='module')
def new_bmi(infile=None):
    try:
        with open('.ROOT_DIR', 'r') as fp:
            root_dir = fp.read()
    except IOError:
        root_dir = '.'

    bmi = Bmi()
    with cd(root_dir):
        bmi.initialize(infile or INPUT_FILE)

    return bmi


def pytest_runtest_setup(item):
    print 'moving folders', item
    # os.chdir('/Users/huttone/git/csdms/bmi-tester/_child_run')


def pytest_generate_tests(metafunc):
    if 'gid' in metafunc.fixturenames:
        metafunc.parametrize('gid', all_grids(new_bmi()))
    elif 'var_name' in metafunc.fixturenames:
        metafunc.parametrize('var_name', all_names(new_bmi()))
    elif 'in_var_name' in metafunc.fixturenames:
        metafunc.parametrize('in_var_name', strictly_input_names(new_bmi()))
    elif 'out_var_name' in metafunc.fixturenames:
        metafunc.parametrize('out_var_name', out_names(new_bmi()))

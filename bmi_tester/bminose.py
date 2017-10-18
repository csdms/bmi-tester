from __future__ import print_function

import sys
import argparse

from .nosetester import BmiTester
from .api import load_component


def run_tests(bmi_cls, infile=None, bmi_version=None, mode='fast',
              verbose=True, doctests=False):
    from . import tests as package

    test = BmiTester(package=package).test

    try:
        package.__dict__['Bmi'] = load_component(bmi_cls)
    except ImportError as err:
        raise

    package.__dict__['INPUT_FILE'] = infile
    if bmi_version is not None:
        package.__dict__['BMI_VERSION_STRING'] = bmi_version

    result = test(label=mode, verbose=verbose,
                  doctests=doctests, # coverage=options.coverage,
                  raise_warnings='release') #, raise_warnings='release')
                  # extra_argv=args, raise_warnings='release') #, raise_warnings='release')

    return result


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('cls', help='Full name of class to test.')
    parser.add_argument('--infile', default='',
                        help='Name of input file for init method.')
    parser.add_argument('--bmi-version', default='1.1',
                        help='BMI version to test against')
    parser.add_argument('-m', '--mode', action='store', dest='mode',
                        default='fast',
                        help='"fast", "full", or something that can be '
                             'passed to nosetests -A')
    parser.add_argument('-v', '--verbose', action='count', dest='verbose',
                        default=1, help='increase verbosity')
    parser.add_argument('--no-doctests', action='store_false', dest='doctests',
                        default=True,
                        help='Do not run doctests in module')

    args = parser.parse_args()

    try:
        result = run_tests(args.cls, infile=args.infile,
                           bmi_version=args.bmi_version, mode=args.mode,
                           verbose=args.verbose, doctests=args.doctests)
    except ImportError as err:
        print('error loading {cls}: {msg}'.format(cls=args.cls, msg=str(err),
                                                  file=sys.stderr))
        sys.exit(-1)
    else:
        if result.wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)

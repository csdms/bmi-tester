from __future__ import print_function

import argparse

from .api import run_test


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cls', help='Full name of class to test.')
    parser.add_argument('--infile', default='',
                        help='Name of input file for init method.')
    parser.add_argument('--out', type=str, default=None,
                        help='Print results to a file.')

    args = parser.parse_args()

    parts = args.cls.split('.')
    mod = '.'.join(parts[:-1])
    cls = parts[-1]

    try:
        results = run_test(args.cls, None, args.infile)
    except ImportError:
        print('unable to import {mod}'.format(mod=mod))

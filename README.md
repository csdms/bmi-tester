# bmi-tester

[anaconda-badge]: https://anaconda.org/conda-forge/bmi-tester/badges/version.svg
[anaconda-link]: https://anaconda.org/conda-forge/bmi-tester
[build-badge]: https://github.com/csdms/bmi-tester/actions/workflows/test.yml/badge.svg
[build-link]: https://github.com/csdms/bmi-tester/actions/workflows/test.yml
[coverage-badge]: https://coveralls.io/repos/github/csdms/bmi-tester/badge.svg
[coverage-link]: https://coveralls.io/github/csdms/bmi-tester
[docs-badge]: https://readthedocs.org/projects/bmi-tester/badge/?version=latest
[docs-link]: https://readthedocs.org/projects/bmi-tester/
[pypi-badge]: https://badge.fury.io/py/bmi-tester.svg
[pypi-link]: https://pypi.org/project/bmi-tester/
[python-badge]: https://img.shields.io/pypi/pyversions/bmi-tester.svg

![[Build Status][build-link]][build-badge]
![[PyPI][pypi-link]][pypi-badge]
![[Anaconda][anaconda-link]][anaconda-badge]
![[Python][pypi-link]][python-badge]
![[Documentation][docs-link]][docs-badge]
![[Coverage][coverage-link]][coverage-badge]

## About

The *bmi-tester* is a command-line utility and Python library for testing
Basic Model Interface (BMI) implementations.

## Requirements

The *bmi-tester* requires Python 3. Additional dependencies can be found
in the project's *requirements.txt* file and can be installed using either
*pip* or *conda*.

In addition to these requirements, the *bmi-tester* also requires the
*gimli.units* package, which is a Python interface to the *udunits2*
C library, which is not available through *pip* but can be installed
using *conda*.

If you are a developer of the *bmi-tester* you will also want to install
additional dependencies for running the project's tests to make sure
that things are working as they should. These dependencies are listed
in *requirements-testing.txt* and can all be install with either *pip*
or *conda*.

## Installation

To install, first create a new environment in which the project will be
installed. This, although not necessary, will isolate the installation
so that there won't be conflicts with your base *Python* installation.
This can be done with *conda* as,

```bash
conda create -n bmi-tester python=3.11
conda activate bmi-tester
```
(Note, this has been tested with Python 3.11, specified above explicitly
for the purpose of using the `pymt_hydrotrend` package as an example (see below).
Higher versions of Python can be selected, and changing the above flag to
`python=3` will instead choose the latest available version.)

### Stable Release

The *bmi-tester*, and its dependencies, can most easily be installed
with *conda*,

```bash
conda install bmi-tester -c conda-forge
```

### From Source

After downloading the *bmi-tester* source code, run the following from
the project's top-level folder (the one that contains *pyproject.toml*) to
install into the current environment,

```bash
pip install -e .
```

## Usage

You can access the *bmi-tester* from the command line with the *bmi-test*
command. Use the *--help* option to get a brief description of the
command line arguments,

```bash
bmi-test --help
```

The *bmi-test* command takes a single argument, the name of the entry point
of the class that implements the BMI you would like to test. To demonstrate
how this works, we will use the *Hydrotrend* model as an example. To install
the Python BMI for *Hydrotrend*, use *conda*,

```bash
conda install pymt_hydrotrend -c conda-forge
```

Once installed, the following will test the BMI implementation for the
*Hydrotrend* class,

```bash
bmi-test pymt_hydrotrend:Hydrotrend
```

The entry point is given as *\<model>:\<class>*. That is, in Python you would
import the *Hydrotrend* class as,

```python
>>> from pymt_hydrotrend import Hydrotrend
```

## Links

- [Source code](http://github.com/csdms/bmi-tester): The
  *bmi-tester* source code repository.
- [Documentation](http://bmi-tester.readthedocs.io/): User
  documentation for *bmi-tester*
- [Get](http://bmi-tester.readthedocs.io/en/latest/getting.html):
  Installation instructions

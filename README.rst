bmi-tester: Test Basic Model Interface implementations
======================================================

|Build Status| |Documentation Status| |Coverage Status| |Conda Version|
|Conda Downloads|

About
-----

The *bmi-tester* is a command-line utility and Python library for testing
Basic Model Interface (BMI) implementations.


Requirements
------------

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


Installation
------------

To install, first create a new environment in which the project will be
installed. This, although not necessary, will isolate the installation
so that there won't be conflicts with your base *Python* installation.
This can be done with *conda* as,

.. code:: bash

  $ conda create -n bmi-tester python=3
  $ conda activate bmi-tester


Stable Release
++++++++++++++

The *bmi-tester*, and its dependencies, can most easily be installed
with *conda*,

.. code:: bash

  $ conda install bmi-tester -c conda-forge

From Source
+++++++++++

After downloading the *bmi-tester* source code, run the following from
the project's top-level folder (the one that contains *pyproject.toml*) to
install into the current environment,

.. code:: bash

  $ pip install -e .

Usage
-----

You can access the *bmi-tester* from the command line with the *bmi-test*
command. Use the *--help* option to get a brief description of the
command line arguments,

.. code:: bash

  $ bmi-test --help

The *bmi-test* command takes a single argument, the name of the entry point
of the class that implements the BMI you would like to test. To demonstrate
how this works, we will use the *Hydrotrend* model as an example. To install
the Python BMI for *Hydrotrend*, use *conda*,

.. code:: bash

  $ conda install pymt_hydrotrend -c conda-forge

Once installed, the following will test the BMI implementation for the
*Hydrotrend* class,

.. code:: bash

  $ bmi-test pymt_hydrotrend:Hydrotrend

The entry point is given as *<model>:<class>*. That is, in Python you would
import the *Hydrotrend* class as,

.. code:: python

  >>> from pymt_hydrotrend import Hydrotrend


Links
-----

-  `Source code <http://github.com/csdms/bmi-tester>`__: The
   *bmi-tester* source code repository.
-  `Documentation <http://bmi-tester.readthedocs.io/>`__: User
   documentation for *bmi-tester*
-  `Get <http://bmi-tester.readthedocs.io/en/latest/getting.html>`__:
   Installation instructions


.. |Build Status| image:: https://github.com/csdms/bmi-tester/actions/workflows/test.yml/badge.svg
   :target: https://github.com/csdms/bmi-tester/actions/workflows/test.yml
.. |Documentation Status| image:: https://readthedocs.org/projects/bmi-tester/badge/?version=latest
   :target: http://bmi-tester.readthedocs.io/en/latest/?badge=latest
.. |Coverage Status| image:: https://coveralls.io/repos/github/csdms/bmi-tester/badge.svg
   :target: https://coveralls.io/github/csdms/bmi-tester
.. |Conda Version| image:: https://anaconda.org/conda-forge/bmi-tester/badges/version.svg
   :target: https://anaconda.org/conda-forge/bmi-tester
.. |Conda Downloads| image:: https://anaconda.org/conda-forge/bmi-tester/badges/downloads.svg
   :target: https://anaconda.org/conda-forge/bmi-tester

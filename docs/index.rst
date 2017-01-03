.. bmi_tester documentation master file, created by
   sphinx-quickstart on Tue Jan  3 11:19:57 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Utilities for testing Python BMI implementaions
===============================================

The `bmi_tester` package provides command-line utilities for testing
a Python classes that implement the Basic Model Interface (BMI).
`bmi_tester` also provides a Python interface to the tester that allows
users to run tests programmatically. The package is also easily
extendable so that new tests can be added to the suite.

Quickstart
----------

Install the ``bmi_tester`` package:

.. code:: bash

    $ conda install bmi_tester -c csdms-stack

This installs the `bmi_tester` package as well as the `bmi-tester`
command. To get help, use the `-h` option:

.. code:: bash

    $ bmi-tester -h

If the class you wish to test is installed (that is, you can run
`from <something> import <class-to-test>`), you can use the
`bmi-tester` command to test your implementation:

.. code:: bash

    $ bmi-tester something.class-to-test


User Guide
----------
.. toctree::
   :maxdepth: 1

   bmi_tester

References
==========

.. [BmiGitHub] BMI on GitHub

  https://github.com/csdms/bmi

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


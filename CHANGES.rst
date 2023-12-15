Changelog for bmi-tester
========================

0.5.7 (unreleased)
------------------

- Nothing changed yet.


0.5.6 (2023-12-15)
------------------

- Fix docs build (#36)

- Updates for Python 3.12 (#35)

- Move static metadata to setup.cfg; update requirements; update CI workflows (#32)


0.5.5 (2021-03-31)
------------------

- Fixed documentation builds on readthedocs (#31)

- Added usage and installation instructions to the README,
  and did a general cleaning up of the docs (#30)

- Fixed a bug when validating some cf-compliant units (#29)

- Added gimli.units as a requirement for unit parsing (#29)

- Added GitHub actions for continuous integration (#28)


0.5.4 (2020-10-31)
------------------

- Removed the test for set_value as it's just too dangerous (#26)

- Fixed tests that use get_grid_node_count on grids that
  are not unstructured (#27)


0.5.3 (2020-10-19)
------------------

- Change tests that use ID arrays (e.g. face_nodes, edge_nodes, etc.) to
  allocate those array buffers as int32 (#25)


0.5.2 (2020-10-09)
------------------

- Fixed a bug in the unstructured grid tests (#24)


0.5.1 (2020-09-10)
------------------

- Fixed the time units check to allow dimensionless units (#22)

- Fixed remaining bmi version strings to 2.0 (#23)

0.5 (2020-09-02)
----------------

- Fixed an error with empty_var_buffer where it returned a read-only array (#20)

- Fixed MANIFEST.in to include necessary source files (#21)

- Added test stages where successive stages depend on one another (#19)

- Cleaned up continuous integration and added Python 3.8 builds (#18)


0.4.4 (2020-03-23)
------------------

- Added test for get_grid_node_count (#17)

0.4.3 (2019-11-12)
------------------


0.4.2 (2019-07-24)
------------------


0.4.1 (2019-05-16)
------------------


0.4.0 (2018-10-25)
------------------


0.3.1 (2018-10-16)
------------------


0.3.0 (2018-09-30)
------------------


0.2.4 (2018-07-04)
------------------


0.2.2 (2018-07-03)
------------------


0.2.1 (2018-06-04)
------------------


0.2 (2018-06-04)
----------------


0.1.0 (2018-04-14)
------------------

- Initial release

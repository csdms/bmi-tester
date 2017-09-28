import numpy as np
from nose.tools import (assert_is_instance, assert_greater_equal,
                        assert_less_equal, assert_almost_equal,
                        assert_greater, assert_in, assert_true, assert_equal)
import cfunits
import standard_names


# import landlab.bmi.components
from . import Component, INPUT_FILE

# Component = landlab.bmi.components.__dict__[NAME]
bmi = Component()


def all_names(bmi):
    return set(bmi.get_input_var_names() + bmi.get_output_var_names())


def all_grids(bmi, gtype=None):
    grids = [bmi.get_var_grid(name) for name in all_names(bmi)]
    if gtype:
        grids = [gid for gid in grids if bmi.get_grid_type(gid) == gtype]
    return set(grids)


def test_get_component_name():
    """Test component name is a string."""
    name = bmi.get_component_name()
    assert_is_instance(name, str)

    return name


def test_has_initialize():
    """Test component has an initialize method."""
    assert_true(hasattr(bmi, 'initialize'))


def test_initialize():
    """Test component can initialize itself."""
    bmi.initialize(INPUT_FILE)


def test_has_finalize():
    """Test component has a finalize method."""
    assert_true(hasattr(bmi, 'finalize'))


def test_var_names():
    """Test var names are valid."""
    bmi.initialize(INPUT_FILE)
    for name in all_names(bmi):
        def _check_is_str(name):
            assert_is_instance(name, str)
        def _check_is_valid(name):
            standard_names.StandardName(name)
        _check_is_str.description = 'Test {name} is str'.format(name=name)
        _check_is_valid.description = 'Test {name} is a Standard Name'.format(name=name)
        yield _check_is_str, name
        yield _check_is_valid, name


def test_get_input_var_names():
    """Input var names is a list of strings."""
    bmi.initialize(INPUT_FILE)
    names = bmi.get_input_var_names()
    assert_is_instance(names, tuple)


def test_get_output_var_names():
    """Output var names is a list of strings."""
    bmi.initialize(INPUT_FILE)
    names = bmi.get_output_var_names()
    assert_is_instance(names, tuple)


def test_get_start_time():
    """Test that there is a start time."""
    bmi.initialize(INPUT_FILE)

    start = bmi.get_start_time()
    time_step = bmi.get_time_step()

    assert_is_instance(start, float)
    assert_almost_equal(start, 0.)


def test_get_time_step():
    """Test that there is a time step."""
    bmi.initialize(INPUT_FILE)
    time_step = bmi.get_time_step()
    assert_is_instance(time_step, float)


def test_time_units_is_str():
    """Test the units of time is a str."""
    bmi.initialize(INPUT_FILE)
    units = bmi.get_time_units()
    assert_is_instance(units, str)


def test_time_units_is_valid():
    """Test the units of time are valid."""
    bmi.initialize(INPUT_FILE)
    units = cfunits.Units(bmi.get_time_units())
    assert_true(units.istime)


def test_get_current_time():
    """Test that there is a current time."""
    bmi.initialize(INPUT_FILE)

    start = bmi.get_start_time()
    now = bmi.get_current_time()
    stop = bmi.get_end_time()

    assert_is_instance(now, (int, float))
    assert_less_equal(now, stop)
    assert_greater_equal(now , start)


def test_get_end_time():
    """Test that there is a stop time."""
    bmi.initialize(INPUT_FILE)

    start = bmi.get_start_time()
    stop = bmi.get_end_time()

    assert_is_instance(stop, (int, float))
    assert_greater_equal(stop, start)


def test_get_grid_rank():
    """Test the rank of the grids."""
    bmi.initialize(INPUT_FILE)

    for name in all_names(bmi):
        def _check_rank(bmi, name):
            rank = bmi.get_grid_rank(name)
            assert_is_instance(rank, int)
            assert_less_equal(rank, 3)
        _check_rank.description = 'Test rank of {name}'.format(name=name)

        yield _check_rank, bmi, name


def test_get_grid_shape():
    """Test the grid shape."""
    """Note: the shape of the grid determines which BMI functions are
    used to access the grid's properties"""
    bmi.initialize(INPUT_FILE)

    for gid in all_grids(bmi, gtype='uniform_rectilinear'):
        def _check_shape(bmi, gid):
            shape = bmi.get_grid_shape(gid)
            assert_is_instance(shape, tuple)
            ndim = len(shape)
            assert_equal(ndim, bmi.get_grid_rank(gid))
            for dim in shape:
                assert_is_instance(dim, int)
        _check_shape.description = "Test grid shape for uniform rectilinear grid {gid}".format(gid=gid)
        yield _check_shape, bmi, gid

    for gid in all_grids(bmi, gtype='scalar'):
        def _check_shape(bmi, gid):
            shape = bmi.get_grid_shape(gid)
            assert_is_instance(shape, tuple)
            np.testing.assert_equal(shape, ())
        _check_shape.description = "Test grid shape for scalar grid {gid}".format(gid=gid)
        yield _check_shape, bmi, gid


def test_get_grid_size():
    for gid in all_grids(bmi):
        def _check_grid_size(bmi, gid):
            size = bmi.get_grid_size(gid)
            assert_is_instance(size, int)
            assert_greater(size, 0)
        _check_grid_size.description = "Test grid size for grid {gid}".format(gid=gid)
        yield _check_grid_size, bmi, gid


def test_get_grid_spacing():
    """Test the grid spacing."""
    for gid in all_grids(bmi, gtype='uniform_rectilinear'):
        def _check_spacing(bmi, gid):
            spacing = bmi.get_grid_spacing(gid)
            assert_is_instance(spacing, tuple)
            ndim = len(spacing)
            assert_equal(ndim, bmi.get_grid_rank(gid))
            for dim in spacing:
                assert_is_instance(dim, (int, float))

        _check_spacing.description = "Test grid spacing for uniform rectilinear grid {gid}".format(gid=gid)
        yield _check_spacing, bmi, gid


def test_get_grid_type():
    """Test the grid type."""

    for gid in all_grids(bmi):
        def _check_type_is_valid(gtype):
            assert_in(gtype, ("scalar", "unstructured", "rectilinear",
                              "structured_quadrilateral",
                              "uniform_rectilinear"))
        _check_type_is_valid.description = "Test grid is known for grid {gid}".format(gid=gid)

        def _check_type_is_str(gtype):
            assert_is_instance(gtype, str)
        _check_type_is_str.description = "Test grid type is str for grid {gid}".format(gid=gid)

        yield _check_type_is_valid, bmi.get_grid_type(gid)
        yield _check_type_is_str, bmi.get_grid_type(gid)


def test_grid_x():
    for gid in all_grids(bmi, gtype='unstructured'):
        def _check_array_is_ndarray(arr):
            assert_is_instance(arr, np.ndarray)
        _check_array_is_ndarray.description = "Test x for grid {gid} is ndarray".format(gid=gid)
        def _check_array_length(arr, size):
            assert_equal(len(arr), size)
        _check_array_length.description = "Test length of x for grid {gid}".format(gid=gid)
        def _check_array_type(arr):
            assert_equal(arr.dtype, np.dtype(float))
        _check_array_length.description = "Test x for grid {gid} is float".format(gid=gid)

        yield _check_array_is_ndarray, bmi.get_grid_x(gid)
        yield _check_array_length, bmi.get_grid_x(gid), bmi.get_grid_size(gid)
        yield _check_array_type, bmi.get_grid_x(gid)


def test_get_input_values():
    """Input values are numpy arrays."""
    names = bmi.get_input_var_names()
    for name in names:
        gid = bmi.get_var_grid(name)
        loc = bmi.get_var_location(name)
        if loc == 'node':
            size = bmi.get_grid_size(gid)
        elif loc == 'edge':
            size = bmi.get_grid_number_of_edges(gid)

        def _check_is_ndarray(arr):
            assert_is_instance(arr, np.ndarray)
        _check_is_ndarray.description = 'Test input {name} is ndarray'.format(name=name)
        def _check_array_length(arr, _size):
            assert_equal(len(arr), _size)
        _check_array_length.description = 'Test input {name} is length {size}'.format(name=name, size=size)

        yield _check_is_ndarray, bmi.get_value(name)
        yield _check_array_length, bmi.get_value(name), size


def test_get_output_values():
    """Output values are numpy arrays."""
    names = bmi.get_output_var_names()
    for name in names:
        gid = bmi.get_var_grid(name)
        loc = bmi.get_var_location(name)
        if loc == 'node':
            size = bmi.get_grid_size(gid)
        elif loc == 'edge':
            size = bmi.get_grid_number_of_edges(gid)
        def _check_is_ndarray(arr):
            assert_is_instance(arr, np.ndarray)
        _check_is_ndarray.description = 'Test output {name} is ndarray'.format(name=name)
        def _check_array_length(arr, _size):
            assert_equal(len(arr), _size)
        _check_array_length.description = 'Test output {name} is length {size}'.format(name=name, size=size)

        yield _check_is_ndarray, bmi.get_value(name)
        yield _check_array_length, bmi.get_value(name), size


def test_get_value_ref():
    """Test if can get reference for value"""
    for name in all_names(bmi):
        def _check_array_is_equal(arr1, arr2):
            np.array_equal(arr1, np.asarray(arr2))
        _check_array_is_equal.description = 'Test array reference for {name}'.format(name=name)
        yield _check_array_is_equal, bmi.get_value(name), bmi.get_value_ref(name)


def test_get_var_grid():
    """Test the grid of the variables."""
    for name in all_grids(bmi):
        gid = bmi.get_var_grid(name)
        def _check_var_grid_is_int(_gid):
            assert_is_instance(_gid, int)
        _check_var_grid_is_int.description = 'Test grid id is int'

        yield _check_var_grid_is_int, gid


def test_get_var_itemsize():
    """Test getting a variable's itemsize"""
    for name in all_names(bmi):
        def _check_var_itemsize(bmi, _name):
            val = bmi.get_value(_name)
            itemsize = val.flatten()[0].nbytes
            np.testing.assert_equal(itemsize, bmi.get_var_itemsize(_name))

        _check_var_itemsize.description = "Test get_var_itemsize for {name}".format(name=name)

        yield _check_var_itemsize, bmi, name


def test_get_var_nbytes():
    """Test getting a variable's nbytes"""
    for name in all_names(bmi):
        def _check_var_nbytes(bmi, _name):
            val = bmi.get_value(_name)
            val_nbytes = val.nbytes
            np.testing.assert_equal(val_nbytes, bmi.get_var_nbytes(_name))

        _check_var_nbytes.description = "Test get_val_nbytes for {name}".format(name=name)

        yield _check_var_nbytes, bmi, name


def test_get_var_type():
    """Test getting a variable's data type"""
    for name in all_names(bmi):
        def _check_var_type(bmi, name):
            val = bmi.get_value(name)
            dtype = bmi.get_var_type(name)
            assert_equal(dtype, type(val.flatten()[0]).__name__)
        _check_var_type.description = "Test get_var_type for {name}".format(name=name)

        yield _check_var_type, bmi, name


def test_get_var_units():
    """Test the units of the variables."""
    for name in all_names(bmi):
        units = bmi.get_var_units(name)
        def _check_units_is_str(units):
            assert_is_instance(units, str)
        def _check_units_is_valid(units):
            cfunits.Units(units)
        _check_units_is_str.description = "Test units for {name} is str".format(name=name)
        _check_units_is_valid.description = "Test units for {name} is valid".format(name=name)

        yield _check_units_is_str, units
        yield _check_units_is_valid, units

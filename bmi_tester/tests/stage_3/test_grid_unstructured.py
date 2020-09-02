import numpy as np
import pytest

from ..conftest import skip_if_grid_type_is


# @pytest.mark.dependency(depends=["test_get_grid_type", "test_get_grid_rank"], scope="session")
def test_grid_x(initialized_bmi, gid):
    skip_if_grid_type_is(initialized_bmi, gid, "uniform_rectilinear")

    gtype = initialized_bmi.get_grid_type(gid)
    ndim = initialized_bmi.get_grid_rank(gid)
    if ndim < 1:
        pytest.skip(f"grid is rank {ndim}")

    if gtype == "unstructured":
        size = initialized_bmi.get_grid_number_of_nodes(gid)
    elif gtype == "rectilinear":
        shape = np.empty(ndim, dtype=np.int32)
        initialized_bmi.get_grid_shape(gid, shape)
        size = shape[-1]

    x = np.full(size, np.nan)
    assert x is initialized_bmi.get_grid_x(gid, x)
    assert np.all(~np.isnan(x))


# @pytest.mark.dependency(depends=["test_get_grid_type", "test_get_grid_rank"], scope="session")
def test_grid_y(initialized_bmi, gid):
    skip_if_grid_type_is(initialized_bmi, gid, "uniform_rectilinear")

    gtype = initialized_bmi.get_grid_type(gid)
    ndim = initialized_bmi.get_grid_rank(gid)
    if ndim < 2:
        pytest.skip(f"grid is rank {ndim}")

    if gtype == "unstructured":
        size = initialized_bmi.get_grid_number_of_nodes(gid)
    elif gtype == "rectilinear":
        shape = np.empty(ndim, dtype=np.int32)
        initialized_bmi.get_grid_shape(gid, shape)
        size = shape[-2]

    y = np.full(size, np.nan)
    assert y is initialized_bmi.get_grid_y(gid, y)
    assert np.all(~np.isnan(y))


# @pytest.mark.dependency(depends=["test_get_grid_type", "test_get_grid_rank"], scope="session")
def test_grid_z(initialized_bmi, gid):
    skip_if_grid_type_is(initialized_bmi, gid, "uniform_rectilinear")

    gtype = initialized_bmi.get_grid_type(gid)
    ndim = initialized_bmi.get_grid_rank(gid)
    if ndim < 3:
        pytest.skip(f"grid is rank {ndim}")

    if gtype == "unstructured":
        size = initialized_bmi.get_grid_number_of_nodes(gid)
    elif gtype == "rectilinear":
        shape = np.empty(ndim, dtype=np.int32)
        initialized_bmi.get_grid_shape(gid, shape)
        size = shape[-3]

    z = np.full(size, np.nan)
    assert z is initialized_bmi.get_grid_z(gid, z)
    assert np.all(~np.isnan(z))

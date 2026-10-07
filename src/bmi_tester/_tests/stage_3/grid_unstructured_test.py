import numpy as np
import pytest

from bmi_tester._utils import skip_if_grid_type_is


def test_grid_x(initialized_bmi, gid, bmi_version):
    skip_if_grid_type_is(initialized_bmi, gid, "uniform_rectilinear")

    gtype = initialized_bmi.get_grid_type(gid)
    ndim = initialized_bmi.get_grid_rank(gid)
    if ndim < 1:
        pytest.skip(f"grid is rank {ndim}")

    if gtype in (
        "unstructured",
        "structured_quadrilateral",
        "points",
    ):
        size = initialized_bmi.get_grid_size(gid)
    elif gtype == "rectilinear":
        shape = np.full(ndim, -1, dtype=np.int32)
        initialized_bmi.get_grid_shape(gid, shape)
        assert np.all(shape > 0)
        size = shape[-1]
    else:
        pytest.skip(f"grid is type {gtype}")

    x = np.full(size, np.nan)
    assert x is initialized_bmi.get_grid_x(gid, x)
    assert np.all(np.isfinite(x))


def test_grid_y(initialized_bmi, gid):
    skip_if_grid_type_is(initialized_bmi, gid, "uniform_rectilinear")

    gtype = initialized_bmi.get_grid_type(gid)
    ndim = initialized_bmi.get_grid_rank(gid)
    if ndim < 2:
        pytest.skip(f"grid is rank {ndim}")

    if gtype in (
        "unstructured",
        "structured_quadrilateral",
        "points",
    ):
        size = initialized_bmi.get_grid_size(gid)
    elif gtype == "rectilinear":
        shape = np.full(ndim, -1, dtype=np.int32)
        initialized_bmi.get_grid_shape(gid, shape)
        assert np.all(shape > 0)
        size = shape[-2]
    else:
        pytest.skip(f"grid is type {gtype}")

    y = np.full(size, np.nan)
    assert y is initialized_bmi.get_grid_y(gid, y)
    assert np.all(np.isfinite(y))


def test_grid_z(initialized_bmi, gid):
    skip_if_grid_type_is(initialized_bmi, gid, "uniform_rectilinear")

    gtype = initialized_bmi.get_grid_type(gid)
    ndim = initialized_bmi.get_grid_rank(gid)
    if ndim < 3:
        pytest.skip(f"grid is rank {ndim}")

    if gtype in (
        "unstructured",
        "structured_quadrilateral",
        "points",
    ):
        size = initialized_bmi.get_grid_size(gid)
    elif gtype == "rectilinear":
        shape = np.full(ndim, -1, dtype=np.int32)
        initialized_bmi.get_grid_shape(gid, shape)
        assert np.all(shape > 0)
        size = shape[-3]
    else:
        pytest.skip(f"grid is type {gtype}")

    z = np.full(size, np.nan)
    assert z is initialized_bmi.get_grid_z(gid, z)
    assert np.all(np.isfinite(z))

import warnings

import numpy as np

from ..conftest import skip_if_grid_type_is_not


# @pytest.mark.dependency(depends=["test_get_grid_rank"], scope="session")
def test_get_grid_shape(initialized_bmi, gid):
    """Test the grid shape."""
    skip_if_grid_type_is_not(
        initialized_bmi,
        gid,
        ("uniform_rectilinear", "rectilinear", "structured_quadrilateral"),
    )

    ndim = initialized_bmi.get_grid_rank(gid)

    shape = np.empty(ndim, dtype=np.int32)
    try:
        rtn = initialized_bmi.get_grid_shape(gid, shape)
    except TypeError:
        warnings.warn("get_grid_shape should take two arguments")
        rtn = initialized_bmi.get_grid_shape(gid)
        shape[:] = rtn
    else:
        assert rtn is shape

    assert np.all(shape > 0)


# @pytest.mark.dependency(depends=["test_get_grid_rank"], scope="session")
def test_get_grid_spacing(initialized_bmi, gid):
    """Test the grid spacing."""
    skip_if_grid_type_is_not(initialized_bmi, gid, "uniform_rectilinear")

    ndim = initialized_bmi.get_grid_rank(gid)

    spacing = np.empty(ndim, dtype=float)
    assert spacing is initialized_bmi.get_grid_spacing(gid, spacing)
    assert np.all(spacing > 0.0)


# @pytest.mark.dependency(depends=["test_get_grid_rank"], scope="session")
def test_get_grid_origin(initialized_bmi, gid):
    """Test the grid origin."""
    skip_if_grid_type_is_not(initialized_bmi, gid, "uniform_rectilinear")

    ndim = initialized_bmi.get_grid_rank(gid)

    spacing = np.empty(ndim, dtype=float)
    assert spacing is initialized_bmi.get_grid_spacing(gid, spacing)
    assert np.all(spacing > 0.0)

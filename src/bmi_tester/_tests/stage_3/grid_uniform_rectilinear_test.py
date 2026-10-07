import numpy as np

from bmi_tester._utils import skip_if_grid_type_is_not


def test_get_grid_shape(initialized_bmi, gid):
    """Test the grid shape."""
    skip_if_grid_type_is_not(
        initialized_bmi,
        gid,
        ("uniform_rectilinear", "rectilinear", "structured_quadrilateral"),
    )

    ndim = initialized_bmi.get_grid_rank(gid)

    shape = np.full(ndim, -1, dtype=np.int32)
    rtn = initialized_bmi.get_grid_shape(gid, shape)
    assert rtn is shape
    assert np.all(shape > 0)

    size = initialized_bmi.get_grid_size(gid)
    assert np.prod(shape) == size


def test_get_grid_spacing(initialized_bmi, gid):
    """Test the grid spacing."""
    skip_if_grid_type_is_not(initialized_bmi, gid, "uniform_rectilinear")

    ndim = initialized_bmi.get_grid_rank(gid)

    spacing = np.full(ndim, -1.0, dtype=float)
    assert spacing is initialized_bmi.get_grid_spacing(gid, spacing)
    assert np.all(spacing > 0.0)
    assert np.all(np.isfinite(spacing))


def test_get_grid_origin(initialized_bmi, gid):
    """Test the grid origin."""
    skip_if_grid_type_is_not(initialized_bmi, gid, "uniform_rectilinear")

    ndim = initialized_bmi.get_grid_rank(gid)

    origin = np.full(ndim, np.nan, dtype=float)
    assert origin is initialized_bmi.get_grid_origin(gid, origin)
    assert np.all(np.isfinite(origin))

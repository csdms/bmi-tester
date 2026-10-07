import numpy as np
import pytest
from packaging.version import Version

from bmi_tester._utils import skip_if_grid_type_is_not
from bmi_tester._utils import skip_if_not_bmi_2

VALID_GRID_TYPES = (
    "none",
    "scalar",
    "vector",
    "unstructured",
    "unstructured_triangular",
    "rectilinear",
    "structured_quadrilateral",
    "uniform_rectilinear",
    "uniform_rectilinear_grid",
)
BMI_2_GRID_TYPES = frozenset(
    {
        "scalar",
        "points",
        "vector",
        "unstructured",
        "structured_quadrilateral",
        "rectilinear",
        "uniform_rectilinear",
    }
)


def test_get_grid_rank(initialized_bmi, gid):
    "Test grid rank for grid"
    rank = initialized_bmi.get_grid_rank(gid)
    assert isinstance(rank, int)
    assert rank <= 3
    assert rank >= 0
    if initialized_bmi.get_grid_type(gid) == "scalar":
        assert rank == 0


def test_get_grid_size(initialized_bmi, gid):
    "Test grid size for grid"
    size = initialized_bmi.get_grid_size(gid)
    assert isinstance(size, int)
    assert size > 0


def test_get_grid_type(initialized_bmi, gid, bmi_version):
    "Test grid is known for grid"
    gtype = initialized_bmi.get_grid_type(gid)
    assert isinstance(gtype, str)
    if bmi_version >= Version("2.0"):
        assert gtype in BMI_2_GRID_TYPES
    else:
        assert gtype in VALID_GRID_TYPES


def test_get_grid_node_count(initialized_bmi, gid, bmi_version):
    "Test number of nodes in grid"
    skip_if_not_bmi_2(bmi_version)
    skip_if_grid_type_is_not(initialized_bmi, gid, "unstructured")

    n_nodes = initialized_bmi.get_grid_node_count(gid)
    assert isinstance(n_nodes, int)
    assert n_nodes > 0


def test_get_grid_edge_count(initialized_bmi, gid, bmi_version):
    "Test number of edges in grid"
    skip_if_not_bmi_2(bmi_version)
    skip_if_grid_type_is_not(initialized_bmi, gid, "unstructured")

    n_edges = initialized_bmi.get_grid_edge_count(gid)
    assert isinstance(n_edges, int)
    assert n_edges >= 0
    if n_edges == 0:
        assert initialized_bmi.get_grid_face_count(gid) == 0


def test_get_grid_face_count(initialized_bmi, gid, bmi_version):
    "Test number of faces in grid"
    skip_if_not_bmi_2(bmi_version)
    skip_if_grid_type_is_not(initialized_bmi, gid, "unstructured")

    n_faces = initialized_bmi.get_grid_face_count(gid)
    assert isinstance(n_faces, int)
    assert n_faces >= 0


def test_get_grid_edge_nodes(initialized_bmi, gid, bmi_version):
    "Test nodes at edges for grid"
    skip_if_not_bmi_2(bmi_version)
    skip_if_grid_type_is_not(initialized_bmi, gid, "unstructured")

    n_edges = initialized_bmi.get_grid_edge_count(gid)
    n_nodes = initialized_bmi.get_grid_node_count(gid)

    if n_edges == 0:
        pytest.skip("grid has no edges")

    edge_nodes = np.full((n_edges, 2), -10, dtype=np.int32).reshape(-1)

    rtn = initialized_bmi.get_grid_edge_nodes(gid, edge_nodes)
    assert rtn is edge_nodes
    assert np.all(edge_nodes >= 0)
    assert np.all(edge_nodes < n_nodes)


@pytest.mark.skip("nodes_per_face")
def test_get_grid_nodes_per_face(initialized_bmi, gid, bmi_version):
    "Test number of nodes at each face for grid"
    skip_if_not_bmi_2(bmi_version)
    skip_if_grid_type_is_not(initialized_bmi, gid, "unstructured")

    n_nodes = initialized_bmi.get_grid_node_count(gid)
    n_faces = initialized_bmi.get_grid_face_count(gid)

    if n_faces == 0:
        pytest.skip("grid has no faces")

    nodes_per_face = np.full(n_faces, -1, dtype=np.int32)

    rtn = initialized_bmi.get_grid_nodes_per_face(gid, nodes_per_face)
    assert rtn is nodes_per_face
    assert np.all(nodes_per_face >= 3)
    assert np.all(nodes_per_face <= n_nodes)


@pytest.mark.skip("face_edges")
def test_get_grid_face_edges(initialized_bmi, gid, bmi_version):
    "Test edges at face for grid"
    skip_if_not_bmi_2(bmi_version)
    skip_if_grid_type_is_not(initialized_bmi, gid, "unstructured")

    n_faces = initialized_bmi.get_grid_face_count(gid)
    n_edges = initialized_bmi.get_grid_edge_count(gid)

    if n_faces == 0:
        pytest.skip("grid has no faces")

    nodes_per_face = np.full(n_faces, -1, dtype=np.int32)
    initialized_bmi.get_grid_nodes_per_face(gid, nodes_per_face)

    face_edges = np.full(nodes_per_face.sum(), -1, dtype=np.int32)

    rtn = initialized_bmi.get_grid_face_edges(gid, face_edges)
    assert rtn is face_edges
    assert np.all(face_edges >= 0)
    assert np.all(face_edges < n_edges)

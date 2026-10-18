from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from numpy.typing import NDArray


@dataclass(eq=False)
class Variable:
    values: NDArray
    grid: int
    location: str
    units: str
    intent: Literal["in", "inout", "out"]


@dataclass
class Time:
    start: float
    end: float
    step: float
    current: float
    units: str


@dataclass(eq=False)
class UnstructuredGrid:
    x: NDArray | None = None
    y: NDArray | None = None
    z: NDArray | None = None
    edge_nodes: NDArray | None = None
    face_edges: NDArray | None = None
    face_nodes: NDArray | None = None
    nodes_per_face: NDArray | None = None
    grid_type: str = "unstructured"


@dataclass
class UniformRectilinearGrid:
    shape: tuple[int, ...]
    spacing: tuple[float, ...]
    origin: tuple[float, ...]
    grid_type: str = "uniform_rectilinear"


@dataclass(eq=False)
class RectilinearGrid:
    x: NDArray | None
    y: NDArray | None
    z: NDArray | None
    grid_type: str = "rectilinear"

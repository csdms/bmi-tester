from __future__ import annotations

import numpy as np

from testing._base import UnstructuredBmi
from testing._data import Time
from testing._data import UnstructuredGrid
from testing._data import Variable


class UnstructuredNodesBmi(UnstructuredBmi):

    def __init__(self):
        self._variables = {
            "land_surface__elevation": Variable(
                values=np.ones(5, dtype=float),
                grid=0,
                location="node",
                units="m",
                intent="inout",
            )
        }

        self._grids = {
            0: UnstructuredGrid(
                x=np.array([0, 1, 2, 0, 1], float),
                y=np.array([0, 0, 0, 1, 1], float),
                z=np.array([2, 2, 2, 2, 2], float),
            ),
        }

        self._time = Time(
            start=0.0,
            end=10.0,
            step=3.0,
            current=0.0,
            units="s",
        )


class PointsBmi(UnstructuredBmi):

    def __init__(self):
        self._variables = {
            "land_surface__elevation": Variable(
                values=np.ones(5, dtype=float),
                grid=0,
                location="node",
                units="m",
                intent="inout",
            )
        }

        self._grids = {
            0: UnstructuredGrid(
                grid_type="points",
                x=np.array([0, 1, 2, 0, 1], float),
                y=np.array([0, 0, 0, 1, 1], float),
                z=np.array([2, 2, 2, 2, 2], float),
            ),
        }

        self._time = Time(
            start=0.0,
            end=10.0,
            step=3.0,
            current=0.0,
            units="s",
        )


class ScalarBmi(UnstructuredBmi):

    def __init__(self):
        self._variables = {
            "land_surface__elevation": Variable(
                values=np.ones(1, dtype=float),
                grid=0,
                location="node",
                units="m",
                intent="inout",
            )
        }

        self._grids = {
            0: UnstructuredGrid(grid_type="scalar"),
        }

        self._time = Time(
            start=0.0,
            end=10.0,
            step=3.0,
            current=0.0,
            units="s",
        )


class UnstructuredNodesEdgesBmi(UnstructuredBmi):
    def __init__(self):
        self._variables = {
            "land_surface__elevation": Variable(
                values=np.ones(5, dtype=float),
                grid=0,
                location="node",
                units="m",
                intent="inout",
            ),
            "land_surface_air__temperature": Variable(
                values=np.ones(6, dtype=float),
                grid=0,
                location="edge",
                units="C",
                intent="in",
            ),
        }

        self._grids = {
            0: UnstructuredGrid(
                x=np.array([0, 1, 2, 0, 1], float),
                y=np.array([0, 0, 0, 1, 1], float),
                z=np.array([2, 2, 2, 2, 2], float),
                edge_nodes=np.asarray(
                    [
                        *[0, 1],
                        *[1, 2],
                        *[0, 3],
                        *[1, 4],
                        *[4, 2],
                        *[3, 4],
                    ],
                    dtype=int,
                ),
            ),
        }

        self._time = Time(
            start=0.0,
            end=10.0,
            step=3.0,
            current=0.0,
            units="s",
        )


class UnstructuredNodesEdgesFacesBmi(UnstructuredBmi):

    def __init__(self):
        self._variables = {
            "land_surface__elevation": Variable(
                values=np.ones(5, dtype=float),
                grid=0,
                location="node",
                units="m",
                intent="inout",
            ),
            "land_surface_air__temperature": Variable(
                values=np.ones(6, dtype=float),
                grid=0,
                location="edge",
                units="C",
                intent="in",
            ),
            "land_surface~10m-above_air_flow__speed": Variable(
                values=np.ones(2, dtype=float),
                grid=0,
                location="face",
                units="m/s",
                intent="out",
            ),
            "air__temperature": Variable(
                values=np.ones(1, dtype=float),
                grid=0,
                location="none",
                units="C",
                intent="inout",
            ),
        }

        self._grids = {
            0: UnstructuredGrid(
                x=np.array([0, 1, 2, 0, 1], float),
                y=np.array([0, 0, 0, 1, 1], float),
                z=np.array([2, 2, 2, 2, 2], float),
                edge_nodes=np.asarray(
                    [
                        *[0, 1],
                        *[1, 2],
                        *[0, 3],
                        *[1, 4],
                        *[4, 2],
                        *[3, 4],
                    ],
                    dtype=int,
                ),
                face_edges=np.asarray(
                    [
                        *[0, 3, 5, 2],
                        *[1, 4, 3],
                    ],
                    dtype=int,
                ),
                face_nodes=np.asarray(
                    [
                        *[0, 1, 4, 3],
                        *[1, 2, 4],
                    ],
                    dtype=int,
                ),
                nodes_per_face=np.asarray([4, 3], dtype=int),
            ),
        }

        self._time = Time(
            start=0.0,
            end=10.0,
            step=3.0,
            current=0.0,
            units="s",
        )

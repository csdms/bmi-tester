from __future__ import annotations

import numpy as np

from testing._base import UniformRectilinearBmi
from testing._data import Time
from testing._data import UniformRectilinearGrid
from testing._data import Variable


class UniformRectilinearExample(UniformRectilinearBmi):

    def __init__(self):
        self._variables = {
            "land_surface__elevation": Variable(
                values=np.ones(12, dtype=float),
                grid=0,
                location="node",
                units="m",
                intent="inout",
            ),
            "land_surface_air__temperature": Variable(
                values=np.ones(12, dtype=float),
                grid=0,
                location="edge",
                units="C",
                intent="in",
            ),
            "land_surface~10m-above_air_flow__speed": Variable(
                values=np.ones(12, dtype=float),
                grid=0,
                location="face",
                units="m/s",
                intent="out",
            ),
        }

        self._grids = {
            0: UniformRectilinearGrid(
                shape=(3, 4, 1),
                spacing=(10.0, 20.0, 1.0),
                origin=(-1.0, 2.0, 1.0),
            )
        }

        self._time = Time(
            start=0.0,
            end=10.0,
            step=3.0,
            current=0.0,
            units="s",
        )

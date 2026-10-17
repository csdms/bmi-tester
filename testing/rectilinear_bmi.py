from __future__ import annotations

import numpy as np

from testing._base import RectilinearBmi
from testing._data import RectilinearGrid
from testing._data import Time
from testing._data import Variable


class RectilinearExample(RectilinearBmi):

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
                values=np.ones(17, dtype=float),
                grid=0,
                location="edge",
                units="C",
                intent="in",
            ),
            "land_surface~10m-above_air_flow__speed": Variable(
                values=np.ones(6, dtype=float),
                grid=0,
                location="face",
                units="m/s",
                intent="out",
            ),
        }

        self._grids = {
            0: RectilinearGrid(
                x=np.array([0, 1, 3, 6], dtype=float),
                y=np.array([0, 1, 2], dtype=float),
                z=np.array([0], dtype=float),
            )
        }

        self._time = Time(
            start=0.0,
            end=10.0,
            step=3.0,
            current=0.0,
            units="s",
        )

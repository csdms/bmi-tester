from __future__ import annotations

import math

from bmipy import Bmi
from numpy.typing import NDArray

from testing._data import RectilinearGrid
from testing._data import Time
from testing._data import UniformRectilinearGrid
from testing._data import UnstructuredGrid
from testing._data import Variable


class BaseBmi(Bmi):

    _variables: dict[str, Variable]
    _time: Time

    def finalize(self) -> None:
        for var in self._variables.values():
            var.values.fill(0.0)

    def get_component_name(self) -> str:
        return "Example BMI"

    def get_current_time(self) -> float:
        return self._time.current

    def get_end_time(self) -> float:
        return self._time.end

    def get_grid_edge_count(self, grid: int) -> int:
        raise NotImplementedError("get_grid_edge_count")

    def get_grid_edge_nodes(self, grid: int, edge_nodes: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_edge_nodes")

    def get_grid_face_count(self, grid: int) -> int:
        raise NotImplementedError("get_grid_face_count")

    def get_grid_face_edges(self, grid: int, face_edges: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_face_edges")

    def get_grid_face_nodes(self, grid: int, face_nodes: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_face_nodes")

    def get_grid_node_count(self, grid: int) -> int:
        raise NotImplementedError("get_grid_node_count")

    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_nodes_per_face")

    def get_grid_origin(self, grid: int, origin: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_origin")

    def get_grid_rank(self, grid: int) -> int:
        raise NotImplementedError("get_grid_rank")

    def get_grid_shape(self, grid: int, shape: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_shape")

    def get_grid_size(self, grid: int) -> int:
        raise NotImplementedError("get_grid_size")

    def get_grid_spacing(self, grid: int, spacing: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_spacing")

    def get_grid_type(self, grid: int) -> str:
        raise NotImplementedError("get_grid_type")

    def get_grid_x(self, grid: int, x: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_x")

    def get_grid_y(self, grid: int, y: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_y")

    def get_grid_z(self, grid: int, z: NDArray) -> NDArray:
        raise NotImplementedError("get_grid_z")

    def get_input_item_count(self) -> int:
        return len(self.get_input_var_names())

    def get_input_var_names(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                name
                for name, var in self._variables.items()
                if var.intent.startswith("in")
            )
        )

    def get_output_item_count(self) -> int:
        return len(self.get_output_var_names())

    def get_output_var_names(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                name
                for name, var in self._variables.items()
                if var.intent.endswith("out")
            )
        )

    def get_start_time(self) -> float:
        return self._time.start

    def get_time_step(self) -> float:
        return self._time.step

    def get_time_units(self) -> str:
        return self._time.units

    def get_value(self, name: str, dest: NDArray) -> NDArray:
        dest[:] = self._variables[name].values
        return dest

    def get_value_at_indices(self, name: str, dest: NDArray, inds: NDArray) -> NDArray:
        dest[:] = self._variables[name].values[inds]
        return dest

    def get_value_ptr(self, name: str) -> NDArray:
        return self._variables[name].values

    def get_var_grid(self, name: str) -> int:
        return self._variables[name].grid

    def get_var_itemsize(self, name: str) -> int:
        return self._variables[name].values.itemsize

    def get_var_location(self, name: str) -> str:
        return self._variables[name].location

    def get_var_nbytes(self, name: str) -> int:
        return self._variables[name].values.nbytes

    def get_var_type(self, name: str) -> str:
        return self._variables[name].values.dtype.name

    def get_var_units(self, name: str) -> str:
        return self._variables[name].units

    def initialize(self, config_file: str) -> None:
        with open(config_file):
            pass

    def set_value(self, name: str, src: NDArray) -> None:
        self._variables[name].values[:] = src

    def set_value_at_indices(self, name: str, inds: NDArray, src: NDArray) -> None:
        self._variables[name].values[inds] = src

    def update(self) -> None:
        raise NotImplementedError("update")

    def update_until(self, time: float) -> None:
        raise NotImplementedError("update_until")


class UnstructuredBmi(BaseBmi):
    _grids: dict[int, UnstructuredGrid]

    def get_grid_edge_count(self, grid: int) -> int:
        values = self._grids[grid].edge_nodes
        return 0 if values is None else len(values.reshape((-1, 2)))

    def get_grid_edge_nodes(self, grid: int, edge_nodes: NDArray) -> NDArray:
        values = self._grids[grid].edge_nodes
        if values is None:
            raise NotImplementedError("get_grid_edge_nodes")
        edge_nodes[:] = values
        return edge_nodes

    def get_grid_face_count(self, grid: int) -> int:
        values = self._grids[grid].nodes_per_face
        return 0 if values is None else len(values)

    def get_grid_face_edges(self, grid: int, face_edges: NDArray) -> NDArray:
        values = self._grids[grid].face_edges
        if values is None:
            raise NotImplementedError("get_grid_face_edges")
        face_edges[:] = values
        return face_edges

    def get_grid_face_nodes(self, grid: int, face_nodes: NDArray) -> NDArray:
        values = self._grids[grid].face_nodes
        if values is None:
            raise NotImplementedError("get_grid_face_nodes")
        face_nodes[:] = values
        return face_nodes

    def get_grid_node_count(self, grid: int) -> int:
        if self.get_grid_rank(grid) > 0:
            return len(self._grids[grid].x)
        raise NotImplementedError("get_grid_node_count")

    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: NDArray) -> NDArray:
        values = self._grids[grid].nodes_per_face
        if values is None:
            raise NotImplementedError("get_grid_nodes_per_face")
        nodes_per_face[:] = values
        return nodes_per_face

    def get_grid_rank(self, grid: int) -> int:
        grid = self._grids[grid]
        return len([dim for dim in (grid.x, grid.y, grid.z) if dim is not None])

    def get_grid_size(self, grid: int) -> int:
        if self.get_grid_rank(grid) > 0:
            return len(self._grids[grid].x)
        return 1

    def get_grid_type(self, grid: int) -> str:
        return self._grids[grid].grid_type

    def get_grid_x(self, grid: int, x: NDArray) -> NDArray:
        values = self._grids[grid].x
        if values is None:
            raise NotImplementedError("get_grid_x")
        x[:] = values
        return x

    def get_grid_y(self, grid: int, y: NDArray) -> NDArray:
        values = self._grids[grid].y
        if values is None:
            raise NotImplementedError("get_grid_y")
        y[:] = values
        return y

    def get_grid_z(self, grid: int, z: NDArray) -> NDArray:
        values = self._grids[grid].z
        if values is None:
            raise NotImplementedError("get_grid_z")
        z[:] = values
        return z


class UniformRectilinearBmi(BaseBmi):

    _grids: dict[int, UniformRectilinearGrid]

    def get_grid_origin(self, grid: int, origin: NDArray) -> NDArray:
        origin[:] = self._grids[grid].origin
        return origin

    def get_grid_rank(self, grid: int) -> int:
        return len(self._grids[grid].shape)

    def get_grid_shape(self, grid: int, shape: NDArray) -> NDArray:
        shape[:] = self._grids[grid].shape
        return shape

    def get_grid_size(self, grid: int) -> int:
        shape = self._grids[grid].shape
        return math.prod(shape) if len(shape) else 0

    def get_grid_spacing(self, grid: int, spacing: NDArray) -> NDArray:
        spacing[:] = self._grids[grid].spacing
        return spacing

    def get_grid_type(self, grid: int) -> str:
        return self._grids[grid].grid_type


class RectilinearBmi(BaseBmi):

    _grids: dict[int, RectilinearGrid]

    def get_grid_rank(self, grid: int) -> int:
        g = self._grids[grid]
        return len([dim for dim in (g.z, g.y, g.x) if dim is not None])

    def get_grid_shape(self, grid: int, shape: NDArray) -> NDArray:
        g = self._grids[grid]
        shape[:] = [len(coord) for coord in (g.z, g.y, g.x) if coord is not None]
        return shape

    def get_grid_size(self, grid: int) -> int:
        g = self._grids[grid]
        shape = [len(coord) for coord in (g.z, g.y, g.x) if coord is not None]
        return math.prod(shape) if len(shape) else 0

    def get_grid_type(self, grid: int) -> str:
        return self._grids[grid].grid_type

    def get_grid_x(self, grid: int, x: NDArray) -> NDArray:
        values = self._grids[grid].x
        if values is None:
            raise NotImplementedError("get_grid_x")
        x[:] = values
        return x

    def get_grid_y(self, grid: int, y: NDArray) -> NDArray:
        values = self._grids[grid].y
        if values is None:
            raise NotImplementedError("get_grid_y")
        y[:] = values
        return y

    def get_grid_z(self, grid: int, z: NDArray) -> NDArray:
        values = self._grids[grid].z
        if values is None:
            raise NotImplementedError("get_grid_z")
        z[:] = values
        return z

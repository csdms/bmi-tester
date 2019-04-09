import numpy as np


class Bmi(object):
    _input_var_names = ("land_surface__elevation", "land_surface_air__temperature")
    _output_var_names = (
        "land_surface__elevation",
        "land_surface~10m-above_air_flow__speed",
    )

    _var_units = {
        "land_surface__elevation": "m",
        "land_surface_air__temperature": "C",
        "land_surface~10m-above_air_flow__speed": "m/s",
    }

    def __init__(self):
        self._values = {
            "land_surface__elevation": np.empty(12, dtype=float),
            "land_surface_air__temperature": np.empty(12, dtype=float),
            "land_surface~10m-above_air_flow__speed": np.empty(12, dtype=float),
        }

    def initialize(self, config_file):
        with open(config_file, "r"):
            pass

    def update(self):
        pass

    def finalize(self):
        pass

    def get_component_name(self):
        return "Test BMI component"

    def get_input_var_names(self):
        return self._input_var_names

    def get_output_var_names(self):
        return self._output_var_names

    def get_current_time(self):
        return 0.0

    def get_start_time(self):
        return 0.0

    def get_end_time(self):
        return 1.0

    def get_time_step(self):
        return 1.0

    def get_time_units(self):
        return "s"

    def get_var_grid(self, name):
        return 0

    def get_var_itemsize(self, name):
        return 8

    def get_var_nbytes(self, name):
        return 8 * 12

    def get_var_type(self, name):
        return "float"

    def get_var_units(self, name):
        return self._var_units[name]

    def get_var_location(self, name):
        return "node"

    def get_grid_rank(self, id_):
        return 2

    def get_grid_size(self, id_):
        return 12

    def get_grid_type(self, id_):
        return "uniform_rectilinear"

    def get_grid_shape(self, id_, shape):
        shape[:] = (3, 4)
        return shape

    def get_grid_spacing(self, id_, spacing):
        spacing[:] = (10.0, 20.0)
        return spacing

    def get_value(self, name, buffer):
        buffer[:] = self._values[name]
        return buffer

    def set_value(self, name, buffer):
        self._values[name][:] = buffer
        return buffer

def all_names(bmi):
    in_names = bmi.get_input_var_names()
    out_names = bmi.get_output_var_names()
    return set(in_names + out_names)


def out_names(bmi):
    out_names = bmi.get_output_var_names()
    return set(out_names)


def in_names(bmi):
    in_names = bmi.get_input_var_names()
    return set(in_names)


def all_grids(bmi, gtype=None):
    grids = set()
    for name in all_names(bmi):
        gid = bmi.get_var_grid(name)
        if gtype == bmi.get_grid_type(gid)[1] or gtype is None:
            grids.add(gid)
    # grids = [bmi.get_var_grid(name) for name in all_names(bmi)]
    # if gtype:
    #     grids = [gid for gid in grids if bmi.get_grid_type(gid) == gtype]
    return grids

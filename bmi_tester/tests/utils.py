import os
import tempfile
import shutil

from scripting.contexts import cd

from . import Bmi, INPUT_FILE


def setup_func():
    # globals().update(bmi=Bmi())
    # bmi.initialize(INPUT_FILE)

    starting_dir = os.path.abspath(os.getcwd())
    tmp_dir = os.path.abspath(tempfile.mkdtemp())
    os.chdir(tmp_dir)
    with open(".ROOT_DIR", "w") as fp:
        fp.write(starting_dir)
    # shutil.copy2(os.path.join(starting_dir, INPUT_FILE), tmp_dir)


def teardown_func():
    # del globals()['bmi']

    tmp_dir = os.path.abspath(os.getcwd())
    with open(".ROOT_DIR", "r") as fp:
        starting_dir = fp.read()

    os.chdir(starting_dir)
    shutil.rmtree(tmp_dir)


def all_names(bmi):
    return set(bmi.get_input_var_names() + bmi.get_output_var_names())


def all_grids(bmi, gtype=None):
    grids = [bmi.get_var_grid(name) for name in all_names(bmi)]
    if gtype:
        grids = [gid for gid in grids if bmi.get_grid_type(gid) == gtype]
    return set(grids)


def new_bmi(infile=None):
    try:
        with open(".ROOT_DIR", "r") as fp:
            root_dir = fp.read()
    except IOError:
        root_dir = "."

    bmi = Bmi()
    with cd(root_dir):
        bmi.initialize(infile or INPUT_FILE)

    return bmi

import os
import importlib


def load_component(entry_point):
    module_name, cls_name = entry_point.split(":")

    component = None
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise
    else:
        try:
            component = module.__dict__[cls_name]
        except KeyError:
            raise ImportError(cls_name)

    return component


# Both of these variables should be overriden to test a particular
# BMI class
Bmi = load_component(os.environ.get("BMITEST_CLASS", None))
INPUT_FILE = os.environ.get("BMITEST_INPUT_FILE", None)
BMI_VERSION_STRING = os.environ.get("BMI_VERSION_STRING", "1.1")

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
try:
    class_to_test = os.environ["BMITEST_CLASS"]
except KeyError:
    Bmi = None
else:
    Bmi = load_component(class_to_test)
INPUT_FILE = os.environ.get("BMITEST_INPUT_FILE", None)
BMI_VERSION_STRING = os.environ.get("BMI_VERSION_STRING", "1.1")

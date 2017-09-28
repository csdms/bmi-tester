import importlib

from .bmitester import BmiTester


def import_class(mod_name, class_name):
    module = importlib.import_module(mod_name)
    cls = module.__dict__[class_name]

    return cls


def run_test(mod_name, class_name, infile):
    cls = import_class(mod_name, class_name)
    tester = BmiTester(cls(), file=infile)
    tester.run()

    return tester.results


def load_component(entry_point):
    module_name, cls_name = entry_point.split(':')

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

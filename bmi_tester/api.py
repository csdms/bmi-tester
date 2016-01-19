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

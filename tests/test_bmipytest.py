from bmi_tester.bmipytest import load_component


entry_point = "os:getcwd"
module_name, cls_name = entry_point.split(":")


def test_component_is_string():
    component = load_component(entry_point)
    assert isinstance(component, str)


def test_component_is_classname():
    component = load_component(entry_point)
    assert component == cls_name

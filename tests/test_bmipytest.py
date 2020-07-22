from bmi_tester.bmipytest import load_component


entry_point = "os:getcwd"
module_name, cls_name = entry_point.split(":")


def test_component_is_not_string():
    component = load_component(entry_point)
    assert not isinstance(component, str)


def test_component_is_classname():
    component = load_component(entry_point)
    assert component.__name__ == cls_name

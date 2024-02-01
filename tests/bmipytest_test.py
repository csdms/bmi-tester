from bmi_tester.main import load_component

entry_point = "os:getcwd"


def test_component_is_not_string():
    component = load_component(entry_point)
    assert not isinstance(component, str)


def test_component_is_classname():
    component = load_component(entry_point)
    _, cls_name = entry_point.split(":")
    assert component.__name__ == cls_name

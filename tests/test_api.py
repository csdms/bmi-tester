import os

from bmi_tester.api import check_bmi


def touch_file(fname):
    with open(fname, "w"):
        pass


def test_bmi_check(tmpdir):
    with tmpdir.as_cwd():
        touch_file("input.yaml")
        assert (
            check_bmi(
                "bmi_tester.bmi:Bmi", input_file="input.yaml", extra_args=["-vvv"]
            )
            == 0
        )


def test_bmi_check_with_manifest_as_list(tmpdir):
    with tmpdir.as_cwd():
        touch_file("input.yaml")
        assert (
            check_bmi(
                "bmi_tester.bmi:Bmi",
                extra_args=["-vvv"],
                input_file="input.yaml",
                manifest=["input.yaml"],
            )
            == 0
        )


def test_bmi_check_with_manifest_as_string(tmpdir):
    with tmpdir.as_cwd():
        with open("manifest.txt", "w") as fp:
            fp.write(os.linesep.join(["input.yaml", "data.dat"]))
        touch_file("input.yaml")
        touch_file("data.dat")
        assert (
            check_bmi(
                "bmi_tester.bmi:Bmi",
                extra_args=["-vvv"],
                input_file="input.yaml",
                manifest="manifest.txt",
            )
            == 0
        )

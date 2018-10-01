from bmi_tester.api import check_bmi


def test_bmi_check(tmpdir):
    with tmpdir.as_cwd():
        with open("input.yaml", "w") as fp:
            pass
        assert (
            check_bmi(
                "bmi_tester.bmi:Bmi", input_file="input.yaml", extra_args=["-vvv"]
            )
            == 0
        )


def test_bmi_check_with_manifest_as_list(tmpdir):
    with tmpdir.as_cwd():
        with open("input.yaml", "w") as fp:
            pass
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
            fp.write("input.yaml")
        with open("input.yaml", "w") as fp:
            pass
        assert (
            check_bmi(
                "bmi_tester.bmi:Bmi",
                extra_args=["-vvv"],
                input_file="input.yaml",
                manifest="manifest.txt",
            )
            == 0
        )

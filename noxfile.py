from __future__ import annotations

import os
import pathlib
import shutil

import nox

PROJECT = "bmi_tester"
ROOT = pathlib.Path(__file__).parent


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[units,testing]")

    session.run("pytest", "tests/")


@nox.session
def coverage(session: nox.Session) -> None:
    """Run coverage."""
    session.install("-e", ".[units,testing]")

    session.run(
        "coverage",
        "run",
        "-m",
        "pytest",
        "tests",
        "--doctest-modules",
        env={"COVERAGE_CORE": "sysmon"},
    )

    session.run("coverage", "report", "--ignore-errors", "--show-missing")
    if "CI" in os.environ:
        session.run("coverage", "xml", "-o", "coverage.xml")


@nox.session(name="test-cli")
def test_cli(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[units,testing]")

    tmpdir = os.path.abspath(session.create_tmp())

    with session.chdir(tmpdir):
        with open("config.toml", "w") as stream:
            print("", file=stream)

        session.run(
            "bmi-test",
            f"--root-dir={tmpdir}",
            "--config-file=config.toml",
            "testing.uniform_rectilinear_bmi:UniformRectilinearExample",
            "-vvv",
            env={"PYTHONPATH": str(ROOT)},
        )


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def build(session: nox.Session) -> None:
    session.install("pip")
    session.install("build")
    session.run("python", "--version")
    session.run("pip", "--version")
    session.run("python", "-m", "build", "--outdir", "./dist")


@nox.session(name="build-docs")
def build_docs(session: nox.Session) -> None:
    """Build the docs."""

    build_generated_docs(session)

    session.install(
        *("-r", "requirements-docs.txt"),
        *("-r", "requirements.txt"),
    )
    session.install(".")

    pathlib.Path("build").mkdir(exist_ok=True)

    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-W",
        "--keep-going",
        "docs",
        "build/html",
    )
    session.log("generated docs at build/html")


@nox.session(name="build-generated-docs", reuse_venv=True)
def build_generated_docs(session: nox.Session) -> None:
    """Build auto-generated files used by the docs."""
    # FOLDER["docs_generated"].mkdir(exist_ok=True)

    session.install("sphinx")
    session.install("-e", ".")

    with session.chdir(ROOT):
        os.makedirs("src/docs/_generated/api", exist_ok=True)
        session.log("generating api docs in docs/api")
        session.run(
            "sphinx-apidoc",
            "-e",
            "-force",
            "--no-toc",
            "--module-first",
            "-o",
            "docs/_generated/api",
            "src/bmi_tester",
        )


@nox.session(python=False)
def clean(session):
    """Remove all .venv's, build files and caches in the directory."""
    folders = (
        (ROOT,) if not session.posargs else (pathlib.Path(f) for f in session.posargs)
    )
    for folder in folders:
        if not str(folder.resolve()).startswith(str(ROOT.resolve())):
            session.log(f"skipping {folder}: folder is outside of repository")
            continue

        with session.chdir(folder):
            session.log(f"cleaning {folder}")

            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("dist", ignore_errors=True)
            shutil.rmtree(f"src/{PROJECT}.egg-info", ignore_errors=True)
            shutil.rmtree(".pytest_cache", ignore_errors=True)
            shutil.rmtree(".venv", ignore_errors=True)

            for pattern in ["*.py[co]", "__pycache__"]:
                _clean_rglob(pattern)


def _clean_rglob(pattern):
    nox_dir = pathlib.Path(".nox")

    for p in pathlib.Path(".").rglob(pattern):
        if nox_dir in p.parents:
            continue
        if p.is_dir():
            p.rmdir()
        else:
            p.unlink()

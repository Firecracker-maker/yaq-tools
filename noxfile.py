import os

import nox

BACKEND = "conda"
REUSE_VENV_IND = True


@nox.session(venv_backend=BACKEND, reuse_venv=REUSE_VENV_IND)
def isort_import_formatting(session):
    args = ["isort"]
    if "black_isort_check" in session.posargs:
        args.append("--check")
    args.extend(["."])
    session.run(*args)


@nox.session(venv_backend=BACKEND, reuse_venv=REUSE_VENV_IND)
def black_code_formatting(session):
    args = ["black"]
    if "black_isort_check" in session.posargs:
        args.append("--check")
    args.extend(["."])
    session.run(*args)


@nox.session(venv_backend=BACKEND, reuse_venv=REUSE_VENV_IND)
def pylint_code_quality(session):
    session.run("pylint", "yaqtools/")


@nox.session(venv_backend=BACKEND, reuse_venv=REUSE_VENV_IND)
def pytest_coverage(session):
    session.run("pylint", "yaqtools/")

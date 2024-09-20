# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import subprocess
import sys
from pathlib import Path

from .conftest import find_script_path

ROOT = Path(__file__).resolve().parent.parent
PY_FILES = sorted(
    str(f)
    for f in list(ROOT.glob("*.py"))
    + list((ROOT / "mozphab").glob("**/*.py"))
    + list((ROOT / "tests").glob("**/*.py"))
)


def test_black():
    print(f"pytest {sys.executable=}")
    print(f"pytest {os.getenv('PYTHONPATH')=}")

    print(subprocess.check_call([sys.executable, "-m", "pip", "freeze"]))

    subprocess.check_call([sys.executable, "-c", "import click"])

    try:
        import click  # noqa: F401

        print("click imported without error")
    except ImportError as e:
        print(f"error importing click: {str(e)}")

    subprocess.check_call([sys.executable, "-m", "black", "--version"])
    subprocess.check_call(["black", "--version"])
    subprocess.check_call([find_script_path("black"), "--version"])
    subprocess.check_call([sys.executable, "-m", "black", "--check"] + PY_FILES)


def test_ruff():
    """Run ruff on the codebase.

    Use the project root as the directory to lint, and define appropriate lint
    paths in the `ruff.toml` file.
    """
    subprocess.check_call(
        (
            find_script_path("ruff"),
            "check",
            "--target-version",
            "py38",
            ROOT,
        )
    )

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pathlib import Path
import subprocess

from .conftest import find_script_path


ROOT = Path(__file__).resolve().parent.parent
PY_FILES = sorted(
    str(f)
    for f in list(ROOT.glob("*.py"))
    + list((ROOT / "mozphab").glob("**/*.py"))
    + list((ROOT / "tests").glob("**/*.py"))
)


def test_black():
    subprocess.check_call([find_script_path("black"), "--check"] + PY_FILES)


def test_ruff():
    """Run ruff on lint paths."""
    for lint_path in PY_FILES:
        subprocess.call(
            (
                find_script_path("ruff"),
                "check",
                "--fix",
                "--target-version",
                "py38",
                lint_path,
            )
        )

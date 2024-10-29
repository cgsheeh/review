# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
from pathlib import Path
from typing import List, Tuple

import pytest

from mozphab.helpers import parse_bugs

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


def get_commit_info() -> List[Tuple[str, str]]:
    git_out = subprocess.run(
        ["git", "log", "origin/main..HEAD", "--pretty=%H %s"],
        capture_output=True,
        text=True,
        check=True,
    )

    return [
        (line.split(" ", 1)[0], line.split(" ", 1)[1])
        for line in git_out.stdout.strip().split("\n")
    ]


@pytest.mark.parametrize("commit_sha,commit_message", get_commit_info())
def test_bug_number(commit_sha: str, commit_message: str):
    """Enforce bug numbers in un-landed commit messages."""
    assert parse_bugs(
        commit_message
    ), f"Commit {commit_sha} does not have a bug number."

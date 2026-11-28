"""Run each project's documented example through both execution paths."""

import json
from pathlib import Path
import re
import subprocess
import sys

import pytest


PROJECTS = Path(__file__).resolve().parents[1] / "projects"
EXAMPLES = sorted(set(PROJECTS.glob("*/main.pa")) - {PROJECTS / "bill-splitter" / "main.pa"})


@pytest.mark.parametrize("source", EXAMPLES, ids=lambda path: path.parent.name)
def test_project_documented_example(source, tmp_path):
    readme = source.with_name("README.md").read_text(encoding="utf-8")
    sample, expected = [
        json.loads(block) for block in re.findall(r"```json\n(.*?)\n```", readme, re.S)
    ]
    stdin = json.dumps(sample) + "\n"
    output = tmp_path / "demo.py"
    compiled = subprocess.run(
        ["nexpro", "compile", str(source), "-o", str(output)],
        capture_output=True, text=True,
    )
    assert compiled.returncode == 0, compiled.stderr
    for command in (["nexpro", "run", str(source)], [sys.executable, "-I", "-S", str(output)]):
        result = subprocess.run(command, input=stdin, text=True, capture_output=True)
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout) == expected


@pytest.mark.parametrize("source", sorted(PROJECTS.glob("*/test_*.pa")), ids=lambda path: path.parent.name)
def test_native_project_assertions(source):
    result = subprocess.run(["nexpro", "run", str(source)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

from importlib.metadata import version
from pathlib import Path
import subprocess
import sys

import pytest


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


@pytest.mark.parametrize(
    ("example", "expected"),
    [
        ("hello", "Hello NexPro!\n"),
        ("variables", "Probal\nKolkata\n"),
        ("math", "30\n10\n200\n2.0\n150\n"),
        ("precedence", "110\n150\n"),
        ("addition", "30\n35\n"),
        ("multiplication", "42\n21.0\n"),
        ("comments", "Comments are ignored\nDone\n"),
        ("math2", "30\n40\n"),
        ("parser1", "Probal\n25\n"),
        ("parser2", "Probal\n20\n"),
        ("strings", "Nex\nPro\n"),
        ("functions", "14\n"),
        ("scope", "17\n10\n100\n"),
        ("temperature", "-40.0\n32.0\n98.6\n"),
        ("greeting", "Hello, NexPro!\n"),
    ],
)
def test_examples(example, expected, tmp_path):
    source = EXAMPLES / f"{example}.pa"
    output = tmp_path / "program.py"

    interpreted = run("nexpro", "run", source, cwd=tmp_path)
    compiled = run("nexpro", "compile", source, "-o", output, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    executed = run(sys.executable, "-I", "-S", output, cwd=tmp_path)

    for result in (interpreted, executed):
        assert result.returncode == 0, result.stderr
        assert result.stdout == expected
        assert not result.stderr


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("say (2 + 3", "Expected ')'"),
        ("say @", "Unknown character"),
        ("function f(x, x) return x end", "Duplicate parameter 'x'"),
        ("function f(x) return x", "Expected 'end'"),
        ("return 1", "Unknown statement"),
    ],
)
def test_invalid_source_preserves_output(source, message, tmp_path):
    program = tmp_path / "program.pa"
    program.write_text(source, encoding="utf-8")
    output = program.with_suffix(".py")
    output.write_text("existing output", encoding="utf-8")
    for command in ("run", "compile"):
        result = run("nexpro", command, program, cwd=tmp_path)
        assert result.returncode == 1
        assert message in result.stderr
        assert str(program) in result.stderr
        assert "Line   : 1" in result.stderr
        assert "Column :" in result.stderr
    assert output.read_text(encoding="utf-8") == "existing output"


@pytest.mark.parametrize(("expression", "message"), [
    ("unknown", "Undefined variable 'unknown'"),
    ("1 / 0", "division by zero"),
    ("missing()", "Undefined function 'missing'"),
    ("twice(1, 2)", "expects 1 argument(s), got 2"),
])
def test_runtime_errors(expression, message, tmp_path):
    source = tmp_path / "broken.pa"
    source.write_text(f"function twice(x) return x * 2 end\nsay {expression}", encoding="utf-8")
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr

    interpreted = run("nexpro", "run", source, cwd=tmp_path)
    executed = run(sys.executable, source.with_suffix(".py"), cwd=tmp_path)
    for result in (interpreted, executed):
        assert result.returncode == 1
        assert message in result.stderr
        assert "Traceback" not in result.stderr


def test_literals_default_output_and_version(tmp_path):
    source = tmp_path / "literals.pa"
    source.write_text(
        'class = "quoted \\"text\\""\nsay class\nsay 0.5 + 1\n',
        encoding="utf-8",
    )
    result = run("nexpro", "compile", source, cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    result = run(sys.executable, source.with_suffix(".py"), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout == 'quoted "text"\n1.5\n'
    result = run("nexpro", "version", cwd=tmp_path)
    assert result.stdout == f"NexPro {version('nexpro')}\n"
    assert version("nexpro") == "0.6.0"


def test_compile_cannot_overwrite_source(tmp_path):
    source = tmp_path / "program.pa"
    source.write_text("say 42", encoding="utf-8")
    result = run("nexpro", "compile", source, "-o", source, cwd=tmp_path)
    assert result.returncode == 1
    assert "must differ" in result.stderr
    assert source.read_text(encoding="utf-8") == "say 42"


def test_long_expression(tmp_path):
    source = tmp_path / "long.pa"
    source.write_text("say " + " + ".join(["1"] * 250), encoding="utf-8")
    result = run("nexpro", "compile", source, cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    result = run(sys.executable, source.with_suffix(".py"), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "250\n"

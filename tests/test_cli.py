from importlib.metadata import version
from pathlib import Path
import subprocess
import sys

import pytest


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def run(*args, cwd, input_text=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, input=input_text)


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
        ("grades", "A\nKeep practicing\ntrue\n"),
        ("multiplication_table", "".join(f"{n * 5}\n" for n in range(1, 11))),
        ("sum_1_to_10", "55\n"),
        (
            "student_report",
            "Ada\nTotal\n255\nAverage\n85.0\nHighest\n100\nLowest\n70\n"
            "Class\nUnassigned\nFields\n['name', 'scores']\n",
        ),
        ("scorecard", "Ada\npassed\n85.0\n"),
        ("score_filter", "85.0\n"),
        ("lists", "6\nNex\no\n30\n"),
        ("imports", "49\n20.0\n"),
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
        ("say ²", "Unknown character"),
        ("function f(x, x) return x end", "Duplicate parameter 'x'"),
        ("function f(x) return x", "Expected 'end'"),
        ("return 1", "Unknown statement"),
        ("break", "only be used inside a loop"),
        ("continue", "only be used inside a loop"),
        ('say {"name" "Ada"}', "Expected ':' after dictionary key"),
        ('say {"name": "Ada"', "Expected '}' after dictionary entries"),
        ("if true say 1", "Expected 'end' after if block"),
        ("while false", "Expected 'end' after while block"),
        ("if true return 1 end", "Unknown statement"),
        ("say [1, 2", "Expected ']' after list elements"),
        ("say [1][0", "Expected ']' after index"),
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
    assert version("nexpro") == "1.7.0"


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


def test_nested_control_flow_and_booleans(tmp_path):
    source = tmp_path / "control.pa"
    source.write_text(
        """
function find()
    index = 0
    while index < 5
        index = index + 1
        if index == 3
            return index
        end
    end
    return 0
end

if false
else
    say find()
end
while false
    say "unreachable"
end
say false
say 2 + 3 * 4 == 14
say 2 != 3
say 3 > 2
say 2 >= 2
say 3 <= 2
""",
        encoding="utf-8",
    )
    compilation = run("nexpro", "compile", source, cwd=tmp_path)
    assert compilation.returncode == 0, compilation.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path),
        run(sys.executable, source.with_suffix(".py"), cwd=tmp_path),
    ):
        assert result.returncode == 0, result.stderr
        assert result.stdout == "3\nfalse\ntrue\ntrue\ntrue\ntrue\nfalse\n"


@pytest.mark.parametrize(("example", "input_text", "expected"), [
    ("clean_names", "  Ada, GRACE, Linus  \n", "ada | grace | linus\n"),
    ("scores", "70\n85\n100\n", "Average\n85.0\nHighest\n100.0\n"),
    ("score_series", "70\n85\n100\n\n", "Average\n85.0\nHighest\n100.0\n"),
    ("score_series", "\n", "No scores\n"),
    ("input", "Ada\n2000\n", "Hello, Ada!\n30\n"),
])
def test_examples_with_input(example, input_text, expected, tmp_path):
    source = EXAMPLES / f"{example}.pa"
    output = tmp_path / "program.py"
    compiled = run("nexpro", "compile", source, "-o", output, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path, input_text=input_text),
        run(sys.executable, "-I", "-S", output, cwd=tmp_path, input_text=input_text),
    ):
        assert result.returncode == 0, result.stderr
        assert result.stdout == expected
        assert not result.stderr


@pytest.mark.parametrize(("source_text", "input_text", "code", "expected"), [
    ('say len([]) say "NexPro"[0] say input("Value: ")', '\n', 0, '0\nN\nValue: \n'),
    ('say [1][2]', '', 1, 'list index out of range'),
    ('say 1[0]', '', 1, 'object is not subscriptable'),
    ('say int(input())', 'abc\n', 1, 'invalid literal'),
    ('say input()', '', 1, 'EOF when reading a line'),
])
def test_data_and_input_boundaries(source_text, input_text, code, expected, tmp_path):
    source = tmp_path / "data.pa"
    source.write_text(source_text, encoding="utf-8")
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path, input_text=input_text),
        run(sys.executable, "-I", "-S", source.with_suffix(".py"), cwd=tmp_path, input_text=input_text),
    ):
        assert result.returncode == code, result.stderr
        if code == 0:
            assert result.stdout == expected
        else:
            assert expected in result.stderr
            assert "Traceback" not in result.stderr


def test_check_does_not_execute_modules(tmp_path):
    source = tmp_path / "main.pa"
    source.write_text('import "module.pa"\nsay input()\n', encoding="utf-8")
    (tmp_path / "module.pa").write_text("say missing()\n", encoding="utf-8")
    result = run("nexpro", "check", source, cwd=tmp_path, input_text="")
    assert result.returncode == 0, result.stderr
    assert result.stdout == "Syntax OK\n"
    assert not result.stderr


def test_nested_modules_are_included_once_and_compiled_inline(tmp_path):
    source = tmp_path / "main.pa"
    source.write_text(
        'import "math/outer.pa"\nimport "./math/inner.pa"\nsay answer()\n',
        encoding="utf-8",
    )
    modules = tmp_path / "math"
    modules.mkdir()
    (modules / "outer.pa").write_text('import "inner.pa"\n', encoding="utf-8")
    (modules / "inner.pa").write_text(
        'say "loaded"\nfunction answer() return 42 end\n', encoding="utf-8",
    )
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    assert run("nexpro", "run", source, cwd=tmp_path).stdout == "loaded\n42\n"
    (modules / "inner.pa").unlink()
    (modules / "outer.pa").unlink()
    standalone = run(sys.executable, "-I", "-S", source.with_suffix(".py"), cwd=tmp_path)
    assert standalone.returncode == 0, standalone.stderr
    assert standalone.stdout == "loaded\n42\n"


@pytest.mark.parametrize(("entry_text", "module_text", "location", "message", "excerpt"), [
    ('import "missing.pa"', '', 'main.pa', "Cannot read module 'missing.pa'", 'import "missing.pa"\n       ^'),
    ('import "../outside.pa"', '', 'main.pa', "inside the entry directory", 'import "../outside.pa"\n       ^'),
    ('import "module.pa"', 'import "main.pa"', 'module.pa', "Circular import", 'import "main.pa"\n       ^'),
    ('import "module.pa"', 'say @', 'module.pa', "Unknown character", 'say @\n    ^'),
    ('import "module.pa"', 'say (3', 'module.pa', "Expected ')'", 'say (3\n      ^'),
])
def test_import_diagnostics(entry_text, module_text, location, message, excerpt, tmp_path):
    source = tmp_path / "main.pa"
    source.write_text(entry_text, encoding="utf-8")
    (tmp_path / "module.pa").write_text(module_text, encoding="utf-8")
    for command in ("check", "run", "compile"):
        result = run("nexpro", command, source, cwd=tmp_path)
        assert result.returncode == 1
        assert not result.stdout
        assert str(tmp_path / location) in result.stderr
        assert message in result.stderr
        assert excerpt in result.stderr
    assert not source.with_suffix(".py").exists()


def test_compile_cannot_overwrite_an_import(tmp_path):
    source = tmp_path / "main.pa"
    module = tmp_path / "module.pa"
    source.write_text('import "module.pa"', encoding="utf-8")
    module.write_text("say 7", encoding="utf-8")
    result = run("nexpro", "compile", source, "-o", module, cwd=tmp_path)
    assert result.returncode == 1
    assert "Output path must differ" in result.stderr
    assert module.read_text(encoding="utf-8") == "say 7"


def test_nested_break_and_loop_scope(tmp_path):
    source = tmp_path / "loops.pa"
    source.write_text("""
for = 7
break = 8
in = 9
values = []
for letter in "ab"
    for item in [1, 2]
        append(values, letter)
        break
    end
end
for untouched in []
    say untouched
end
say values
say for + break + in
""", encoding="utf-8")
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path),
        run(sys.executable, "-I", "-S", source.with_suffix(".py"), cwd=tmp_path),
    ):
        assert result.returncode == 0, result.stderr
        assert result.stdout == "['a', 'b']\n24\n"


def test_runtime_stack_points_to_imported_source(tmp_path):
    entry = tmp_path / "main.pa"
    module = tmp_path / "math.pa"
    entry.write_text('import "math.pa"\nsay outer()\n', encoding="utf-8")
    module.write_text(
        "function inner()\n    return 1 / 0\nend\n"
        "function outer()\n    return inner()\nend\n",
        encoding="utf-8",
    )
    compiled = run("nexpro", "compile", entry, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", entry, cwd=tmp_path),
        run(sys.executable, "-I", "-S", entry.with_suffix(".py"), cwd=tmp_path),
    ):
        assert result.returncode == 1
        assert result.stderr.splitlines() == [
            "NexPro Runtime Error: division by zero",
            f"  at inner ({module}:2)",
            f"  at outer ({module}:5)",
            f"  at <program> ({entry}:2)",
        ]


def test_short_circuit_precedence_and_continue(tmp_path):
    source = tmp_path / "logic.pa"
    source.write_text("""
say false and missing()
say true or missing()
say not 1 == 1 or false and missing()
say not [] and (true or missing())
continue = 7
say continue
i = 0
while i < 3
    i = i + 1
    if i != 2
        continue
    end
    say i
end
""", encoding="utf-8")
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path),
        run(sys.executable, "-I", "-S", source.with_suffix(".py"), cwd=tmp_path),
    ):
        assert result.returncode == 0, result.stderr
        assert result.stdout == "false\ntrue\nfalse\ntrue\n7\n2\n"


@pytest.mark.parametrize(("source_text", "expected", "code"), [
    (
        'data = {"x": [3], "y": 2, "y": 5}\n'
        'data["x"][0] = 7\n'
        'for key in data say key end\n'
        'say data["x"][0] + data["y"]\n'
        'say len({})',
        'x\ny\n12\n0\n',
        0,
    ),
    ('say {}["missing"]', "'missing'", 1),
    ('say {[]: 1, "unused": missing()}', "unhashable type: 'list'", 1),
    ('text = "x"\ntext[0] = "y"', "does not support item assignment", 1),
])
def test_dictionary_and_item_assignment(source_text, expected, code, tmp_path):
    source = tmp_path / "dict.pa"
    source.write_text(source_text, encoding="utf-8")
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path),
        run(sys.executable, "-I", "-S", source.with_suffix(".py"), cwd=tmp_path),
    ):
        assert result.returncode == code, result.stderr
        if code == 0:
            assert result.stdout == expected
        else:
            assert expected in result.stderr
            assert "Traceback" not in result.stderr


@pytest.mark.parametrize(("code", "expected", "status"), [
    ('say sum([]) say sum([1, -2, 0.5])', '0\n-0.5\n', 0),
    ('say keys({}) say keys({"z": 1, "a": 2})', "[]\n['z', 'a']\n", 0),
    ('say get({"x": 0}, "x", 9) say get({}, "x", 9)', '0\n9\n', 0),
    ('function sum(items) return 9 end say sum([])', '9\n', 0),
    ('say min([])', 'min() requires at least one item', 1),
    ('say max([])', 'max() requires at least one item', 1),
    ('say sum([true])', 'sum() expects a list of numbers', 1),
    ('say min(["2", 3])', 'min() expects a list of numbers', 1),
    ('say max("text")', 'max() expects a list of numbers', 1),
    ('say keys([])', 'keys() expects a dictionary', 1),
    ('say get([], "x", 0)', 'get() expects a dictionary', 1),
    ('say get({}, [], 0)', "unhashable type: 'list'", 1),
    ('say get({}, "x")', 'missing 1 required positional argument', 1),
])
def test_data_builtins(code, expected, status, tmp_path):
    source = tmp_path / "data.pa"
    source.write_text(code, encoding="utf-8")
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path),
        run(sys.executable, "-I", "-S", source.with_suffix(".py"), cwd=tmp_path),
    ):
        assert result.returncode == status, result.stderr
        if status == 0:
            assert result.stdout == expected
            assert not result.stderr
        else:
            assert expected in result.stderr
            assert f"({source}:1)" in result.stderr
            assert "Traceback" not in result.stderr


@pytest.mark.parametrize(("code", "expected", "status"), [
    ('say trim("  বাংলা　") say lower("ÉCOLE") say upper("straße")', 'বাংলা\nécole\nSTRASSE\n', 0),
    ('say split("", ",") say split(",x,,", ",")', "['']\n['', 'x', '', '']\n", 0),
    ('say join([], ",") say join(["আ", "লো"], "")', '\nআলো\n', 0),
    ('say split("x", "")', 'non-empty separator', 1),
    ('say split("x", 1)', 'expects a text separator', 1),
    ('say join([1], ",")', 'expects a list of text values', 1),
    ('say join(["x"], 0)', 'expects a text separator', 1),
    ('say trim(1)', 'trim() expects text', 1),
])
def test_text_builtins(code, expected, status, tmp_path):
    source = tmp_path / "text.pa"
    source.write_text(code, encoding="utf-8")
    compiled = run("nexpro", "compile", source, cwd=tmp_path)
    assert compiled.returncode == 0, compiled.stderr
    for result in (
        run("nexpro", "run", source, cwd=tmp_path),
        run(sys.executable, "-I", "-S", source.with_suffix(".py"), cwd=tmp_path),
    ):
        assert result.returncode == status, result.stderr
        if status == 0:
            assert result.stdout == expected
        else:
            assert expected in result.stderr

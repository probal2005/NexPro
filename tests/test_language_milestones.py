import json
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
run_playground = runpy.run_path(str(ROOT / "web/playground.py"))["run_playground"]


def check_runtimes(source, expected):
    result = json.loads(run_playground(source, "run"))
    assert result == {"ok": True, "output": expected}
    compiled = json.loads(run_playground(source, "compile"))
    assert compiled["ok"]
    with TemporaryDirectory() as directory:
        script = Path(directory) / "compiled.py"
        script.write_text(compiled["output"], encoding="utf-8")
        process = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert (process.returncode, process.stdout, process.stderr) == (0, expected, "")


def test_invoice_defaults_null_and_elif():
    source = (ROOT / "examples/invoice_total.pa").read_text(encoding="utf-8")
    check_runtimes(source, "2000\n1800\nNo discount supplied\n")
    check_runtimes(source.replace('json.parse("null")', "25"), "2000\n1800\n1500\n")
    check_runtimes(source.replace('json.parse("null")', '"bad"'), "2000\n1800\nInvalid discount\n")


def test_defaults_are_evaluated_in_order_and_per_call():
    check_runtimes("""
function resolve(x, y = x + 1, values = [])
    append(values, y)
    return values
end
say resolve(4)
say resolve(9)
say resolve(4, null)
say type_of(null)
if null
    say "wrong"
end
""", "[5]\n[10]\n[None]\nnull\n")
    invalid = json.loads(run_playground("function invalid(a = 1, b) end", "check"))
    assert not invalid["ok"]
    assert "Required parameters must precede" in invalid["error"]

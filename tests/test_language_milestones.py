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


def test_try_catches_nested_failures_and_preserves_control_flow():
    check_runtimes("""
function validate(value)
    if value < 0
        throw "Negative value"
    end
    return value
end

for number in [-1, 1, 2, 3]
    try
        value = validate(number)
        if value == 1
            continue
        elif value == 3
            break
        end
        say value
    catch message
        say message
    end
end
say message
try
    say int("invalid")
catch bad_conversion
    say "Invalid number"
end
""", "Negative value\n2\nNegative value\nInvalid number\n")


def test_unhandled_throw_includes_the_source_location():
    source = 'function fail()\n    throw "no stock"\nend\nfail()'
    result = json.loads(run_playground(source, "run"))
    assert not result["ok"]
    assert "NexPro Runtime Error: no stock" in result["error"]
    assert "playground.pa:2" in result["error"]
    assert "playground.pa:4" in result["error"]


def test_queue_and_statistics():
    source = (ROOT / "examples/dispatch_summary.pa").read_text(encoding="utf-8")
    check_runtimes(source, "{'North': 2, 'South': 1}\n6\n6\n")
    check_runtimes("""
import "std/queue" as queue
import "std/stats" as stats
pending = queue.new()
queue.enqueue(pending, "A")
queue.enqueue(pending, "B")
say queue.peek(pending)
say queue.dequeue(pending)
say queue.to_list(pending)
say type_of(pending)
say stats.count_by([])
say stats.median([3, 7])
try
    say stats.mean([])
catch error
    say "Empty sample"
end
""", "A\nA\n['B']\nqueue\n{}\n5.0\nEmpty sample\n")


def test_linked_list_operations_keep_head_and_tail_consistent():
    check_runtimes("""
import "std/linked_list" as links
items = links.new([2, 4])
links.insert(items, 0, 1)
links.insert(items, 2, 3)
links.insert(items, 4, 5)
say links.to_list(items)
say links.remove(items, 4)
say links.remove(items, 0)
say links.remove(items, 1)
say links.remove(items, 0)
say links.remove(items, 0)
links.append(items, 9)
say links.to_list(items)
say len(items)
say type_of(items)
try
    links.remove(items, -1)
catch error
    say "Invalid index"
end
""", "[1, 2, 3, 4, 5]\n5\n1\n3\n2\n4\n[9]\n1\nlinked_list\nInvalid index\n")

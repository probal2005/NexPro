import json
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
run_playground = runpy.run_path(str(ROOT / "web/playground.py"))["run_playground"]


def check_runtimes(source, expected, modules=None):
    modules_json = json.dumps(modules or {})
    result = json.loads(run_playground(source, "run", modules_json=modules_json))
    assert result == {"ok": True, "output": expected}
    compiled = json.loads(run_playground(source, "compile", modules_json=modules_json))
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


def test_structured_error_includes_origin_and_preserves_message_catches():
    check_runtimes('''function fail()
    throw "no_stock", "No stock"
end
try
    fail()
catch (error)
    say error["code"]
    say error["message"]
    say error["file"]
    say error["line"]
    say error["function"]
end
try
    fail()
catch message
    say message
end
''', "no_stock\nNo stock\nplayground.pa\n2\nfail\nNo stock\n")


def test_structured_inventory_distinguishes_bad_rows_from_missing_columns():
    source = (ROOT / "examples/structured_inventory.pa").read_text(encoding="utf-8")
    check_runtimes(source, "Skipped row 3: invalid_integer\n10\nStopped: csv_missing_columns\n")


def test_named_arguments_fill_optional_and_required_slots():
    source = (ROOT / "examples/named_invoice.pa").read_text(encoding="utf-8")
    check_runtimes(source, "1800\n1250\n")
    check_runtimes("""
function total(first, discount = first // 10, fee = 0)
    return first - discount + fee
end
say total(fee = 25, first = 100)
try
    total(10, first = 20)
catch message
    say message
end
try
    total(other = 10)
catch message
    say message
end
try
    total(fee = 10)
catch message
    say message
end
""", "115\nFunction 'total' got multiple values for 'first'\n"
         "Function 'total' has no parameter 'other'\nFunction 'total' is missing required argument 'first'\n")


def test_named_argument_order_and_duplicates_are_checked_at_parse_time():
    for source in ("f(a = 1, a = 2)", "f(a = 1, 2)"):
        assert not json.loads(run_playground(source, "check"))["ok"]


def test_record_defaults_fixed_fields_and_json():
    source = (ROOT / "examples/invoice_record.pa").read_text(encoding="utf-8")
    check_runtimes(source, 'record\nUSD\n{"number": "INV-001", "amount_cents": 1800, '
                           '"currency": "USD", "paid": true}\nmissing_key\n')
    check_runtimes("""
import "std/dict" as records
record Item(sku, history = [])
first = Item("A")
second = Item(sku = "B")
append(first["history"], 1)
say len(second["history"])
try
    records.remove(first, "sku")
catch message
    say message
end
say first["sku"]
ordinary = {}
ordinary["new"] = true
say ordinary["new"]
""", "0\nCannot remove field 'sku' from record 'Item'\nA\ntrue\n")


def test_aliased_module_exports_named_function_and_record():
    modules = {"models.pa": """record Item(sku, count = 0)
function make(sku, count = 1)
    return Item(count = count, sku = sku)
end
"""}
    source = '''import "models.pa" as models
say models.make(count = 7, sku = "A")["count"]
say models.Item(sku = "B")["count"]
'''
    check_runtimes(source, "7\n0\n", modules)


def test_typed_record_rejects_invalid_assignment_without_changing_the_value():
    source = (ROOT / "examples/typed_invoice.pa").read_text(encoding="utf-8")
    check_runtimes(source, "record_field_type\namount_cents\n1800\ntrue\n")


def test_typed_record_checks_required_values_defaults_and_error_details():
    check_runtimes("""record Invoice(amount: integer, paid: boolean = "no")
try
    Invoice(true, false)
catch (error)
    say error["details"]["record"]
    say error["details"]["field"]
    say error["details"]["expected"]
    say error["details"]["actual"]
    say error["line"]
end
try
    Invoice(1800)
catch (error)
    say error["details"]["field"]
end
invoice = Invoice(amount = 1800, paid = false)
say invoice["paid"]
record Flexible(metadata, missing: null = null)
instance = Flexible("text")
instance["metadata"] = 42
say instance["metadata"]
say instance["missing"]
""", "Invoice\namount\ninteger\nboolean\n3\npaid\nfalse\n42\nnull\n")
    invalid = json.loads(run_playground("record Invoice(amount: money)", "check"))
    assert not invalid["ok"]
    assert "supported record field type" in invalid["error"]


def test_record_dot_access_shares_storage_and_validation_with_indexing():
    source = (ROOT / "examples/record_fields.pa").read_text(encoding="utf-8")
    check_runtimes(source, "true\nrecord_field_type\n1800\n")
    check_runtimes("""
import "models.pa" as models
values = [models.sample]
values[0].amount = 5
say models.sample.amount
record Order(invoice: record)
order = Order(values[0])
order.invoice.amount = 9
say order.invoice["amount"]
say models.create()["amount"]
try
    models.sample = 3
catch error
    say error
end
""", "5\n9\n7\nCannot assign directly to a module export.\n", {
        "models.pa": """record Invoice(amount: integer)
sample = Invoice(2)
function create()
    return Invoice(7)
end
""",
    })

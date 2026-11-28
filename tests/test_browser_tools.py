import json
import runpy
from pathlib import Path

from nexpro.compiler import compile_program
from nexpro.loader import load_program

ROOT = Path(__file__).resolve().parents[1]
run_playground = runpy.run_path(str(ROOT / "web/playground.py"))["run_playground"]


def test_form_results_use_current_field_values():
    source = (ROOT / "examples/tool_bill.pa").read_text()
    response = json.loads(run_playground(
        source, "preview", fields_json='{"Bill total": 20, "People": 3}'
    ))
    assert response["ok"]
    assert response["tool"]["fields"][0]["value"] == 20
    assert response["tool"]["results"] == [
        {"label": "Base share", "value": "6.66"},
        {"label": "People paying one extra cent", "value": "2"},
        {"label": "Share with extra cent", "value": "6.67"},
    ]
    invalid = json.loads(run_playground(source, "preview", fields_json='{"People": 0}'))
    assert not invalid["ok"]
    assert "Enter a whole number from 1 to 10000" in invalid["error"]


def test_csv_preserves_quoted_cells_in_both_runtimes(capsys):
    source = '''import "std/csv" as csv
import "std/json" as json
cells = csv.parse(json.parse(input()))
say csv.stringify(cells)
'''
    csv = 'name,notes\r\n"আদা, Inc.","line 1\r\nline 2"\r\n'
    input_line = json.dumps(csv)
    response = json.loads(run_playground(source, "run", input_line))
    assert response == {"ok": True, "output": csv + "\n"}

    tree = load_program("test.pa", lambda name: source)
    from unittest.mock import patch

    with patch("builtins.input", return_value=input_line):
        exec(compile_program(tree), {"__name__": "__main__"})
    assert capsys.readouterr().out == response["output"]


def test_csv_rejects_missing_columns():
    source = 'import "std/csv" as csv\nsay csv.parse(input())\n'
    response = json.loads(run_playground(source, "run", "name,name"))
    assert not response["ok"]
    assert "column names must be unique" in response["error"]


def test_quote_form_options_and_custom_validation():
    source = (ROOT / "examples/tool_quote.pa").read_text()
    fields = {"Client": " ", "Currency": "BDT", "Include expenses": False}
    invalid = json.loads(run_playground(source, "preview", fields_json=json.dumps(fields)))["tool"]
    assert invalid["errors"] == {"Client": "Enter a client name."}
    assert invalid["results"] == []
    fields["Client"] = "Ada"
    valid = json.loads(run_playground(source, "preview", fields_json=json.dumps(fields)))["tool"]
    assert valid["errors"] == {}
    assert {row["label"]: row["value"] for row in valid["results"]}["Total quote"] == "400"


def test_inventory_form_reports_columns_and_rows_and_names_the_download():
    source = (ROOT / "examples/tool_inventory.pa").read_text()

    def tool(csv):
        return json.loads(run_playground(source, "preview", fields_json=json.dumps({"Stock CSV": csv})))["tool"]

    assert "Missing CSV columns" in tool("sku,stock\nA,2\n")["errors"]["Stock CSV"]
    invalid = tool("sku,stock,minimum,target\nA,2,4,10\nB,broken,4,10\n")
    assert "CSV data row 2" in invalid["errors"]["Stock CSV"]
    assert invalid["downloads"] == {}
    valid = tool('sku,stock,minimum,target\n"আদা, A",2,4,10\n')
    assert valid["downloads"] == {"reorder.csv": 'sku,quantity\r\n"আদা, A",8\r\n'}

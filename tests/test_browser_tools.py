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
    assert "People must be at least 1" in invalid["error"]


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

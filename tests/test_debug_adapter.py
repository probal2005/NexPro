"""Exercise the released debugger over the same protocol used by VS Code."""

import json
import queue
import subprocess
import threading


def test_debug_adapter_pauses_in_imported_function_and_steps(tmp_path):
    module = tmp_path / "math.pa"
    module.write_text(
        "function square(value)\n    result = value * value\n    return result\nend\n",
        encoding="utf-8",
    )
    program = tmp_path / "main.pa"
    program.write_text('import "math.pa" as math\nsay math.square(4)\n', encoding="utf-8")
    messages = queue.Queue()

    with subprocess.Popen(["nexpro", "debug-adapter"], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as child:
        def reader():
            while (header := child.stdout.readline()):
                size = int(header.split(b":", 1)[1])
                assert child.stdout.readline() == b"\r\n"
                messages.put(json.loads(child.stdout.read(size)))

        thread = threading.Thread(target=reader, daemon=True)
        thread.start()
        sequence = 0
        events = []

        def request(command, arguments=None):
            nonlocal sequence
            sequence += 1
            payload = json.dumps({
                "seq": sequence, "type": "request", "command": command,
                "arguments": arguments or {},
            }).encode("utf-8")
            child.stdin.write(f"Content-Length: {len(payload)}\r\n\r\n".encode() + payload)
            child.stdin.flush()
            while True:
                message = messages.get(timeout=10)
                if message["type"] == "event":
                    events.append(message)
                else:
                    assert message["request_seq"] == sequence
                    assert message["success"], message
                    return message.get("body", {})

        def event(name):
            for index, message in enumerate(events):
                if message["event"] == name:
                    return events.pop(index)["body"]
            while True:
                message = messages.get(timeout=10)
                if message["event"] == name:
                    return message["body"]
                events.append(message)

        try:
            request("initialize")
            request("launch", {"program": str(program)})
            event("initialized")
            request("setBreakpoints", {"source": {"path": str(module)}, "breakpoints": [{"line": 2}]})
            request("configurationDone")
            assert event("stopped")["reason"] == "breakpoint"
            assert request("stackTrace")["stackFrames"][0]["line"] == 2
            assert request("variables", {"variablesReference": 1})["variables"][0]["value"] == "4"
            request("stepIn")
            assert event("stopped")["reason"] == "step"
            assert request("stackTrace")["stackFrames"][0]["line"] == 3
            locals_ = request("variables", {"variablesReference": 1})["variables"]
            assert {item["name"]: item["value"] for item in locals_} == {"value": "4", "result": "16"}
            request("continue")
            assert event("exited")["exitCode"] == 0
            assert "".join(item["body"]["output"] for item in events if item["event"] == "output") == "16\n"
            request("disconnect")
        finally:
            if child.poll() is None:
                child.terminate()

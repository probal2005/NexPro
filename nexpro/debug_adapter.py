"""Debug Adapter Protocol service for the NexPro interpreter."""

import io
import json
import sys
import threading
from contextlib import redirect_stdout
from pathlib import Path

from nexpro.interpreter import Interpreter


class DebugOutput(io.TextIOBase):
    def __init__(self, send):
        self.send = send

    def write(self, text):
        if text:
            self.send("output", {"category": "stdout", "output": text})
        return len(text)


class DebugAdapter:
    def __init__(self, read, write, load):
        self.read = read
        self.write = write
        self.load = load
        self.writing = threading.Lock()
        self.condition = threading.Condition()
        self.sequence = 0
        self.breakpoints = {}
        self.launch = None
        self.worker = None
        self.paused = False
        self.stepping = False
        self.step_depth = None
        self.current_depth = 0
        self.stop_reason = "step"
        self.cancelled = False
        self.snapshot = None

    def send(self, message):
        with self.writing:
            self.sequence += 1
            body = json.dumps({"seq": self.sequence, **message}).encode("utf-8")
            self.write.write(f"Content-Length: {len(body)}\r\n\r\n".encode() + body)
            self.write.flush()

    def event(self, name, body=None):
        self.send({"type": "event", "event": name, "body": body or {}})

    def receive(self):
        headers = {}
        while True:
            line = self.read.readline()
            if not line:
                return None
            if line in (b"\n", b"\r\n"):
                break
            key, value = line.decode("ascii").split(":", 1)
            headers[key.lower()] = value.strip()
        size = int(headers.get("content-length", "0"))
        if not 0 < size <= 4 * 1024 * 1024:
            raise ValueError("Invalid debug protocol message size")
        return json.loads(self.read.read(size))

    def response(self, request, body=None, error=None):
        message = {
            "type": "response", "request_seq": request["seq"],
            "command": request["command"], "success": error is None,
        }
        if error is not None:
            message["message"] = error
        else:
            message["body"] = body or {}
        self.send(message)

    def observe(self, interpreter, statement):
        if statement.location is None:
            return
        filename, line = statement.location
        filename = str(Path(filename).resolve())
        with self.condition:
            if self.cancelled:
                raise InterruptedError("Debug session ended")
            at_breakpoint = line in self.breakpoints.get(filename, ())
            eligible_step = self.stepping and (
                self.step_depth is None or interpreter.function_depth <= self.step_depth
            )
            if not eligible_step and not at_breakpoint:
                return
            self.stepping = False
            self.current_depth = interpreter.function_depth
            self.paused = True
            local = interpreter.runtime.dump()
            global_values = interpreter.globals.dump()
            self.snapshot = filename, line, interpreter.function_name, local, global_values
            self.event("stopped", {
                "reason": "breakpoint" if at_breakpoint else self.stop_reason,
                "threadId": 1, "allThreadsStopped": True,
            })
            self.condition.wait_for(lambda: not self.paused or self.cancelled)
            if self.cancelled:
                raise InterruptedError("Debug session ended")

    def execute(self):
        code = 0
        try:
            program = self.load(Path(self.launch["program"]).resolve())
            inputs = iter(self.launch.get("input", "").splitlines())

            def read_input(prompt=""):
                if prompt:
                    self.event("output", {"category": "stdout", "output": str(prompt)})
                try:
                    return next(inputs)
                except StopIteration:
                    raise EOFError("No debugger input remains. Set input in launch.json.") from None

            with redirect_stdout(DebugOutput(self.event)):
                Interpreter(read_input=read_input, observer=self.observe).visit(program)
        except InterruptedError:
            code = 1
        except Exception as error:
            code = 1
            self.event("output", {"category": "stderr", "output": str(error) + "\n"})
        finally:
            self.event("exited", {"exitCode": code})
            self.event("terminated")

    def handle(self, request):
        command = request["command"]
        args = request.get("arguments", {})
        if command == "initialize":
            self.response(request, {"supportsConfigurationDoneRequest": True})
        elif command == "launch":
            if self.launch is not None or not isinstance(args.get("program"), str):
                raise ValueError("A NexPro program path is required")
            self.launch = args
            self.stepping = bool(args.get("stopOnEntry"))
            self.stop_reason = "entry"
            self.response(request)
            self.event("initialized")
        elif command == "setBreakpoints":
            filename = str(Path(args["source"]["path"]).resolve())
            lines = [item["line"] for item in args.get("breakpoints", [])]
            with self.condition:
                self.breakpoints[filename] = set(lines)
            self.response(request, {"breakpoints": [
                {"verified": line > 0, "line": line} for line in lines
            ]})
        elif command == "setExceptionBreakpoints":
            self.response(request)
        elif command == "configurationDone":
            if self.launch is None or self.worker is not None:
                raise ValueError("Launch must precede configuration")
            self.response(request)
            self.worker = threading.Thread(target=self.execute, daemon=True)
            self.worker.start()
        elif command == "threads":
            self.response(request, {"threads": [{"id": 1, "name": "NexPro"}]})
        elif command in ("continue", "stepIn", "stepOut", "next", "pause"):
            with self.condition:
                self.stepping = command != "continue"
                self.stop_reason = "pause" if command == "pause" else "step"
                self.step_depth = {
                    "next": self.current_depth,
                    "stepOut": self.current_depth - 1,
                }.get(command)
                self.response(request, {"allThreadsContinued": True} if command == "continue" else {})
                if command != "pause":
                    self.paused = False
                    self.snapshot = None
                    self.condition.notify_all()
        elif command in ("stackTrace", "scopes", "variables"):
            with self.condition:
                snapshot = self.snapshot
            if snapshot is None:
                raise ValueError("Program is not stopped")
            filename, line, name, local, globals_ = snapshot
            if command == "stackTrace":
                self.response(request, {"stackFrames": [{
                    "id": 1, "name": name, "line": line, "column": 1,
                    "source": {"name": Path(filename).name, "path": filename},
                }], "totalFrames": 1})
            elif command == "scopes":
                self.response(request, {"scopes": [
                    {"name": "Locals", "variablesReference": 1, "expensive": False},
                    {"name": "Globals", "variablesReference": 2, "expensive": False},
                ]})
            else:
                values = local if args["variablesReference"] == 1 else globals_
                self.response(request, {"variables": [
                    {"name": key, "value": repr(value), "variablesReference": 0}
                    for key, value in values.items()
                ]})
        elif command in ("disconnect", "terminate"):
            self.response(request)
            return False
        else:
            self.response(request, error=f"Unsupported debug request: {command}")
        return True

    def serve(self):
        try:
            while (request := self.receive()) is not None:
                if request.get("type") != "request":
                    continue
                try:
                    if not self.handle(request):
                        break
                except (ValueError, KeyError, TypeError, OSError) as error:
                    self.response(request, error=str(error))
        finally:
            with self.condition:
                self.cancelled = True
                self.condition.notify_all()
            if self.worker is not None:
                self.worker.join(timeout=1)


def serve_debug_adapter(load):
    DebugAdapter(sys.stdin.buffer, sys.stdout.buffer, load).serve()

"""Reproducible end-to-end benchmarks for the NexPro CLI."""

from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from time import perf_counter


def benchmark(root, name, source, expected):
    entry = root / f"{name}.pa"
    entry.write_text(source, encoding="utf-8")
    start = perf_counter()
    result = run(["nexpro", "run", str(entry)], capture_output=True, text=True, check=True)
    run_seconds = perf_counter() - start
    start = perf_counter()
    run(["nexpro", "compile", str(entry)], capture_output=True, text=True, check=True)
    compile_seconds = perf_counter() - start
    if result.stdout != expected:
        raise ValueError(f"{name} produced incorrect output: {result.stdout!r}")
    print(f"{name}: run {run_seconds:.3f}s, compile {compile_seconds:.3f}s")


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        benchmark(root, "large_list", "say sum(range(100000))\n", "4999950000\n")
        for index in range(60):
            (root / f"module_{index}.pa").write_text(f"value = {index}\n", encoding="utf-8")
        imports = "".join(f'import "module_{i}.pa" as m{i}\n' for i in range(60))
        benchmark(root, "multi_file", imports + "say m0.value + m59.value\n", "59\n")
        benchmark(root, "long_run", """
total = 0
for value in range(75000)
    total = total + value
end
say total
""", "2812462500\n")


if __name__ == "__main__":
    main()

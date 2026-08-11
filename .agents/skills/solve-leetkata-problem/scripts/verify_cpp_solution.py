#!/usr/bin/env python3
"""Compile a LeetCode-style C++ solution fragment and optionally run its test harness."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode == 0:
        return
    if completed.stdout:
        print(completed.stdout, file=sys.stderr, end="")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    raise SystemExit(completed.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile a LeetCode-style solution fragment; optionally compile and run a test harness."
    )
    parser.add_argument("solution", type=Path, help="path to the solution .cpp file")
    parser.add_argument("--test", type=Path, help="path to a standalone test .cpp file")
    parser.add_argument("--compiler", help="C++ compiler (defaults to g++ or clang++)")
    parser.add_argument("--standard", default="c++20", help="C++ standard (default: c++20)")
    args = parser.parse_args()

    solution = args.solution.resolve()
    if not solution.is_file():
        parser.error(f"solution does not exist: {solution}")
    if solution.suffix != ".cpp":
        parser.error("solution must have a .cpp extension")

    compiler = args.compiler or shutil.which("g++") or shutil.which("clang++")
    if not compiler:
        parser.error("no C++ compiler found; use --compiler to specify one")

    flags = [compiler, f"-std={args.standard}", "-Wall", "-Wextra", "-Wpedantic"]
    with tempfile.TemporaryDirectory(prefix="leetkatas-cpp-") as temporary_directory:
        temporary = Path(temporary_directory)
        if args.test:
            test = args.test.resolve()
            if not test.is_file():
                parser.error(f"test does not exist: {test}")
            executable = temporary / "solution_test"
            run([*flags, str(test), "-o", str(executable)])
            run([str(executable)])
            print(f"PASS: compiled and ran {test}")
            return

        wrapper = temporary / "compile_check.cpp"
        wrapper.write_text(
            "#include <bits/stdc++.h>\n"
            "using namespace std;\n\n"
            f'#include "{solution.as_posix()}"\n\n'
            "int main() { return 0; }\n",
            encoding="utf-8",
        )
        executable = temporary / "compile_check"
        run([*flags, str(wrapper), "-o", str(executable)])
        print(f"PASS: compiled {solution}")


if __name__ == "__main__":
    main()

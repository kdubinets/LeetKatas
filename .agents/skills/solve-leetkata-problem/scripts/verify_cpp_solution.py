#!/usr/bin/env python3
"""Compile a LeetCode-style C++ solution fragment and optionally run its test harness."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_TIMEOUT_SECONDS = 60.0

SANITIZER_FLAGS = [
    "-fsanitize=address,undefined",
    "-fno-sanitize-recover=all",
    "-fno-omit-frame-pointer",
    "-g",
]


# LeetCode preincludes these helper structs for linked-list and binary-tree problems, so
# a solution may reference them without defining them. `Node` is deliberately absent: it
# names a different shape per problem (random-pointer list, N-ary tree, quad tree), so
# there is no single definition to supply.
LEETCODE_HELPER_TYPES: dict[str, str] = {
    "ListNode": (
        "struct ListNode {\n"
        "    int val;\n"
        "    ListNode *next;\n"
        "    ListNode() : val(0), next(nullptr) {}\n"
        "    ListNode(int x) : val(x), next(nullptr) {}\n"
        "    ListNode(int x, ListNode *next) : val(x), next(next) {}\n"
        "};\n"
    ),
    "TreeNode": (
        "struct TreeNode {\n"
        "    int val;\n"
        "    TreeNode *left;\n"
        "    TreeNode *right;\n"
        "    TreeNode() : val(0), left(nullptr), right(nullptr) {}\n"
        "    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n"
        "    TreeNode(int x, TreeNode *left, TreeNode *right)\n"
        "        : val(x), left(left), right(right) {}\n"
        "};\n"
    ),
}


def helper_type_preamble(source: str) -> str:
    """Supply helper structs the solution references but does not define itself."""
    definitions = [
        definition
        for name, definition in LEETCODE_HELPER_TYPES.items()
        if re.search(rf"\b{name}\b", source)
        and not re.search(rf"^\s*(?:struct|class)\s+{name}\b", source, re.MULTILINE)
    ]
    return "\n".join(definitions)


def emit(completed_stdout: str, completed_stderr: str) -> None:
    """Send captured child output to stderr so it never pollutes protocol stdout."""
    if completed_stdout:
        print(completed_stdout, file=sys.stderr, end="")
    if completed_stderr:
        print(completed_stderr, file=sys.stderr, end="")


def run(command: list[str], timeout: float | None = None) -> None:
    """Run a command, always surfacing its diagnostics, and exit on failure.

    Compiler warnings arrive on a zero exit code, so output is forwarded even when the
    command succeeds; warnings stay non-fatal unless the caller compiled with -Werror.
    """
    try:
        completed = subprocess.run(
            command, text=True, capture_output=True, timeout=timeout
        )
    except subprocess.TimeoutExpired as expired:
        emit(expired.stdout or "", expired.stderr or "")
        print(
            f"FAIL: timed out after {timeout:g}s running {' '.join(command)}",
            file=sys.stderr,
        )
        raise SystemExit(124) from None
    emit(completed.stdout, completed.stderr)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile a LeetCode-style solution fragment; optionally compile and run a test harness."
    )
    parser.add_argument("solution", type=Path, help="path to the solution .cpp file")
    parser.add_argument("--test", type=Path, help="path to a standalone test .cpp file")
    parser.add_argument("--compiler", help="C++ compiler (defaults to g++ or clang++)")
    parser.add_argument("--standard", default="c++20", help="C++ standard (default: c++20)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat compiler warnings as errors (-Werror); off by default",
    )
    parser.add_argument(
        "--no-sanitize",
        action="store_true",
        help="omit AddressSanitizer/UndefinedBehaviorSanitizer from the --test build",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"seconds allowed for the compiled test binary (default: {DEFAULT_TIMEOUT_SECONDS:g})",
    )
    args = parser.parse_args()

    solution = args.solution.resolve()
    if not solution.is_file():
        parser.error(f"solution does not exist: {solution}")
    if solution.suffix != ".cpp":
        parser.error("solution must have a .cpp extension")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    compiler = args.compiler or shutil.which("g++") or shutil.which("clang++")
    if not compiler:
        parser.error("no C++ compiler found; use --compiler to specify one")

    flags = [compiler, f"-std={args.standard}", "-Wall", "-Wextra", "-Wpedantic"]
    if args.strict:
        flags.append("-Werror")
    with tempfile.TemporaryDirectory(prefix="leetkatas-cpp-") as temporary_directory:
        temporary = Path(temporary_directory)
        if args.test:
            test = args.test.resolve()
            if not test.is_file():
                parser.error(f"test does not exist: {test}")
            # Sanitizers only pay off here: this is the one path that runs the binary.
            test_flags = flags if args.no_sanitize else [*flags, *SANITIZER_FLAGS]
            executable = temporary / "solution_test"
            run([*test_flags, str(test), "-o", str(executable)])
            run([str(executable)], timeout=args.timeout)
            print(f"PASS: compiled and ran {test}")
            return

        # The wrapper deliberately mimics the LeetCode environment: <bits/stdc++.h> plus
        # `using namespace std;` are exactly what LeetCode preincludes, so a solution that
        # relies on them compiles here as it would there. DO NOT "fix" this by trimming the
        # header or the using-directive. Two consequences are accepted by design:
        #   1. This check cannot detect missing-include defects in the solution.
        #   2. <bits/stdc++.h> is a GCC libstdc++ extension, so the clang++ fallback may
        #      fail to find it on toolchains without libstdc++ headers.
        # Helper structs LeetCode preincludes (ListNode, TreeNode) are supplied the same
        # way when referenced and not self-defined; without them this path fails on every
        # linked-list and tree problem. Problems using a bare `Node` remain unsupported
        # here — see LEETCODE_HELPER_TYPES — and must be verified through --test.
        wrapper = temporary / "compile_check.cpp"
        preamble = helper_type_preamble(solution.read_text(encoding="utf-8"))
        wrapper.write_text(
            "#include <bits/stdc++.h>\n"
            "using namespace std;\n\n"
            + (f"{preamble}\n" if preamble else "")
            + f'#include "{solution.as_posix()}"\n\n'
            + "int main() { return 0; }\n",
            encoding="utf-8",
        )
        executable = temporary / "compile_check"
        run([*flags, str(wrapper), "-o", str(executable)])
        print(f"PASS: compiled {solution}")


if __name__ == "__main__":
    main()

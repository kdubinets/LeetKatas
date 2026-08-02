# LeetKatas Development Guide

## Scope and ownership

- `src/nvim-driver/` owns the Neovim session state, process bridge, UI, launcher, and headless workflow.
- `src/scripts/` owns exercise selection, compilation and review orchestration, reviewer adapters, scheduling, and SQLite persistence.
- `practice/cpp/` owns C++ exercise collections and has additional rules in its nested `AGENTS.md`.
- `.agents/skills/` contains project-specific Codex workflows.
- Preserve unrelated and untracked datasets, generated problem files, logs, and user changes. Do not treat a dirty worktree as disposable.

## Python environment

Use the project virtual environment at `.venv`. The launcher prefers it automatically unless `PRACTICE_PYTHON` is set.

When running tests, put `.venv/bin` first on `PATH` because script integration tests invoke `python3` in subprocesses:

```bash
PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest discover -s src/scripts/tests -v
```

Install declared Python dependencies with:

```bash
.venv/bin/python -m pip install -r src/nvim-driver/requirements.txt
```

## Protocol invariants

- Script entry points read one JSON object from stdin and write one JSON response to stdout.
- Keep diagnostic text inside the JSON response or on stderr; never mix progress messages into protocol stdout.
- A learner compilation failure is a valid evaluation result, not a command-level failure.
- Compilation and LLM review are separate stages; review still runs after compilation failure.
- Keep `proposed_rating` nullable when review is unavailable. In Lua, JSON `null` becomes `vim.NIL`, which is truthy; type-check before string operations or rating acceptance.
- External reviewers read one JSON request from stdin and return one schema-valid JSON review on stdout. Tests must use deterministic fake reviewers rather than live LLM calls.
- Preserve the generic reviewer contract when changing the Codex adapter.

## Progress and diagnostics

- Evaluator stdout is reserved for the final response. Send live progress through the temporary JSONL progress channel.
- Keep the progress pane truthful: report actual compiler/reviewer events, attempts, and retry delays rather than guessed stages.
- Persistent practice logs must not contain submitted source, metadata bodies, credentials, environment secrets, or database contents.
- Codex stderr may echo its prompt; do not copy complete reviewer failures into persistent logs.
- Preserve session IDs, process lifecycle records, compact response summaries, and Lua callback tracebacks when changing logging.

## Verification

After Python or protocol changes, run the complete Python suite. After launcher changes, run shellcheck:

```bash
shellcheck src/nvim-driver/practice
```

After Neovim workflow or UI changes, run the headless workflow with temporary state and the fake reviewer:

```bash
test_db=$(mktemp --suffix=.sqlite3)
test_log=$(mktemp)
PRACTICE_AUTOSTART=0 \
PRACTICE_DATABASE="$test_db" \
PRACTICE_LOG="$test_log" \
PRACTICE_REVIEWER="$PWD/src/nvim-driver/tests/fake_reviewer.py" \
PATH="$PWD/.venv/bin:$PATH" \
nvim --headless --clean -u src/nvim-driver/init.lua \
  -l src/nvim-driver/tests/headless.lua
```

Snap-packaged Neovim may require sandbox escalation. Do not replace the fake reviewer with Codex merely to validate the normal workflow.

Run `git diff --check` before handing off changes.

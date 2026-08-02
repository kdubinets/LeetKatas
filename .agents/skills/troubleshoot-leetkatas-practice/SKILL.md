---
name: troubleshoot-leetkatas-practice
description: Diagnose failures in the LeetKatas C++ Neovim practice driver, compiler evaluation, LLM reviewer harness, rating persistence, launcher, or FSRS scheduling. Use when a user says practice failed, hung, showed unavailable feedback, selected incorrectly, could not record a rating, or otherwise behaved unexpectedly—even when they provide no diagnostic output.
---

# Troubleshoot LeetKatas Practice

Diagnose from persistent evidence first. Ask the user for copied output only after exhausting local logs and reproducible checks.

## Locate the installation and evidence

1. Resolve the repository with `git rev-parse --show-toplevel` and verify it contains `src/nvim-driver/practice`.
2. Read the newest JSONL entries from `$PRACTICE_LOG` when set; otherwise inspect `${XDG_STATE_HOME:-$HOME/.local/state}/nvim/leetkatas/practice.log` and its `.1` rotation. Neovim's actual `stdpath("state")` may vary, so use `nvim --headless --clean +'lua print(vim.fn.stdpath("state"))' +qa` if needed.
3. Group records by `session_id`. Start with the newest session unless the user gives an approximate time or ID.
4. Resolve the practice database from `PRACTICE_DATABASE`, then `$XDG_DATA_HOME/leetkatas/practice.sqlite3`, and finally `~/.local/share/leetkatas/practice.sqlite3`. For review-content questions, inspect the matching `reviews` and `review_artifacts` rows with SQLite read-only mode. The artifact archive contains the submitted source and complete structured reviewer response for rated attempts until its TTL expires.
5. Read `references/subsystems.md` when the failing boundary is unclear.

Do not expose submitted source, metadata, credentials, environment secrets, or unrelated database contents in the response. The normal log intentionally omits source and metadata bodies. Archived artifacts are sensitive: first inspect presence, timestamps, sizes, JSON validity, model, reasoning effort, status, and expected response fields. Read source or feedback bodies only when necessary for the user's question, and summarize rather than reproducing them.

An absent artifact does not by itself indicate a persistence bug. Check whether the review predates archive schema version 4, the archive TTL expired, `review_archive_ttl_days` was zero, or the evaluation was skipped without recording a rating.

## Triage the event sequence

Follow one session chronologically:

1. Find `session_started` and notifications indicating the last user-visible state.
2. Pair each `process_started` with `process_finished` by script and order.
3. Inspect `exit_code`, `signal`, `duration_ms`, `stderr`, `decode_error`, and compact `response`.
4. For review-quality or missing-feedback reports, correlate the review row with its artifact. Verify that persisted model and reasoning effort agree with the archived response, then inspect the structured feedback fields relevant to the report.
5. Classify the failing boundary: launcher/environment, selection/SQLite/FSRS, compiler, reviewer protocol/Codex, Neovim response validation/UI, rating persistence, or artifact archival/retention.
6. State the evidence and root cause before changing code. Implement a fix only when the user requested one or the active request clearly includes repair.

## Reproduce safely

Use the project venv and preserve user data:

```bash
PATH="$PWD/.venv/bin:$PATH" python -m unittest discover -s src/scripts/tests -v
shellcheck src/nvim-driver/practice
```

Use a temporary database and log for headless Neovim. Set `PRACTICE_REVIEWER` to `src/nvim-driver/tests/fake_reviewer.py` to avoid live LLM calls. Snap-packaged Neovim may require sandbox escalation.

For reviewer failures, run these in order:

```bash
.venv/bin/python src/scripts/codex_reviewer.py --check
codex --version
```

Then reproduce `evaluate_exercise.py` with temporary starter, submission, metadata, and a deterministic reviewer. Do not send live exercise evidence to Codex unless reproducing the real adapter is necessary and within scope.

## Common signatures

- `FSRS dependency is unavailable`: compare `PRACTICE_PYTHON`, launcher selection, `command -v python3`, and `.venv/bin/python -c 'import fsrs'`.
- `invalid_json_schema`: inspect `SCHEMA` in `src/scripts/codex_reviewer.py`; Codex strict schemas require complete properties and `additionalProperties: false`.
- `proposed_rating` userdata errors: JSON `null` decodes as `vim.NIL`; normalize or type-check before string operations.
- `review.status = unavailable`: inspect `review.failure` and attempt count; distinguish missing executable/authentication/configuration from timeout, nonzero exit, malformed JSON, and schema-invalid output.
- invalid evaluator response: compare `session.lua` validation against the evaluator's exact JSON shape and `vim.NIL` handling.
- rating failure: inspect `record_rating.py`, schema version/migration, nullable proposal, reviewer metadata, and SQLite transaction errors.
- missing archived review: inspect schema version, configured TTL, whether a rating was recorded, `review_artifacts.expires_at`, and the database file mode. Review artifacts are purged on a subsequent rating rather than by a background timer.
- unexpected reviewer model or effort: compare the compact evaluator response, `reviews.reviewer_model` and `reviews.reviewer_reasoning_effort`, and the archived response's `model` and `reasoning_effort` fields.

## Verify and report

Run focused tests first, then Python unit tests, shellcheck, and the headless workflow. Report the session ID or review ID, relevant event sequence, artifact availability when applicable, root cause, changed files, and verification. If evidence is insufficient, ask only for the missing item and tell the user how to obtain it with `:PracticeDiagnostics` or `:PracticeLog`.

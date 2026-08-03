# Practice Workflow Scripts

This directory contains the editor-independent Python commands used by the
Neovim practice driver:

- `select_exercise.py` selects a due or unseen exercise from a collection.
- `evaluate_exercise.py` evaluates a submitted working copy.
- `record_rating.py` records the final rating and updates its FSRS card.
- `practice_stats.py` reports collection state, workload, forecasts, timing, and history.
- `load_practice_config.py` validates and normalizes the optional user TOML file.
- `practice_scheduler.py` provides shared FSRS and SQLite behavior.
- `sync_progress.py` optionally synchronizes the append-only review ledger to Supabase.
- `prompts/` contains adapter-specific reviewer instructions.

The commands communicate with callers through stable JSON input and output
contracts. Language-specific discovery and evaluation behavior belongs here,
while `src/nvim-driver` owns only Neovim workflow and presentation concerns.

Each command reads one JSON object from standard input and writes one JSON
object to standard output. A nonzero exit status means the command or request
failed. An exercise that does not compile is a successful evaluation command
whose `compiled` field is `false`.

Relative paths returned by `load_practice_config.py` are resolved against the
directory containing the configuration file.

## Protocols

`select_exercise.py` accepts:

```json
{
  "exercise_directory": "/absolute/or/relative/path",
  "source_extension": ".cpp",
  "metadata_extension": ".md",
  "previous_exercise_id": "optional-basename",
  "database_path": "optional-database-override"
}
```

It returns an `exercise` object containing `id`, `source_path`, and
`metadata_path`. When the collection contains a valid `environment.json`, the
object also contains its structured `target_environment`. The paths are
absolute. The oldest due exercise is selected
first. When none is due and `exercise_order.md` exists, unseen exercises follow
its line order. The file contains one unadorned exercise basename per line and
must cover every discovered exercise exactly once. Collections without the file
retain random unseen selection. The
previous exercise is excluded when an alternative of the same scheduling class
is available. When every exercise has scheduling state and none is due, the
command returns `exercise: null` and the UTC `next_due` timestamp.

`evaluate_exercise.py` accepts source and metadata paths, an optional structured
`target_environment`, and a command array. One or more arguments must contain
the literal `{source}` placeholder. The command is executed directly without a
shell.

```json
{
  "source_path": "/temporary/working-copy.cpp",
  "metadata_path": "/collection/exercise.md",
  "target_environment": {
    "language": {
      "name": "C++",
      "version": "C++20"
    }
  },
  "command": ["g++", "-std=c++20", "-fsyntax-only", "{source}"]
}
```

It returns `compiled`, `diagnostics`, raw `metadata`, additive
`metadata_sections`, structured reviewer state, and a nullable
`proposed_rating`. `metadata_sections` is a best-effort ordered parse of
level-one headings, prose, and fenced code. Sections and blocks carry one-based
source line information, and code blocks retain their language. Malformed or
legacy metadata may produce an empty or partial parse while raw `metadata`
remains the compatibility fallback. Validation success is evidence for the reviewer;
it does not determine the rating by itself. Reviewer executables receive the
starter and submitted source, exercise metadata, optional target environment,
and a language-neutral `validation` object containing `command`, `succeeded`,
and `diagnostics`.

The Codex adapter reads its instructions from
`prompts/codex_reviewer.txt`. Other reviewer adapters can use independent prompt
files without changing the generic reviewer request or response contract.

`review_follow_up.py` provides a separate conversational contract. It accepts
the original evidence, initial review, up to sixteen alternating history
messages, the latest `question`, and a separately configured reviewer command.
The external follow-up reviewer returns `{"answer":"..."}`; the bridge adds
availability, attempt, reviewer, model, and reasoning-effort metadata. The
Codex adapter selects this contract with `--follow-up` and reads its independent
instructions from `prompts/codex_review_follow_up.txt`.

`record_rating.py` accepts:

```json
{
  "exercise_directory": "/collection/path",
  "exercise_id": "exercise-basename",
  "compiled": true,
  "proposed_rating": "good",
  "final_rating": "excellent",
  "reviewer_model": "gpt-5.6-luna",
  "reviewer_reasoning_effort": "low",
  "submitted_source": "int solve() { return 1; }\n",
  "review_response": {"status": "available", "feedback": {}},
  "solve_duration_ms": 12500,
  "feedback_duration_ms": 3200,
  "review_archive_ttl_days": 30,
  "database_path": "optional-database-override"
}
```

It maps `fail`, `acceptable`, `good`, and `excellent` to FSRS Again, Hard, Good,
and Easy. The updated card and immutable review log are committed together,
including reviewer model and reasoning effort when provided. A successful
response contains `recorded`, the next UTC `due` timestamp, and the card
`state`. When submission and review artifacts are supplied, they are stored in
`review_artifacts` for the configured TTL and expired artifacts are purged by a
subsequent rating. A TTL of zero disables new artifact storage.

The two duration fields are optional for compatibility with older callers, but
must be supplied together as non-negative integer milliseconds. New Neovim
sessions use them for active solve and feedback-reading time.

`practice_stats.py` accepts an exercise directory, database path, source and
metadata extensions, and a history length (30 days in the Neovim UI). It returns
today, collection-state, seven-day forecast, and daily-history objects. Calendar
dates use the process's local timezone while stored review timestamps remain UTC.

If `database_path` is omitted, both scheduler commands use
`PRACTICE_DATABASE`, then `$XDG_DATA_HOME/leetkatas/practice.sqlite3`, and
finally `~/.local/share/leetkatas/practice.sqlite3`.

## Optional Supabase backup and synchronization

SQLite remains authoritative for every interactive operation. A collection is
syncable only when it has a valid `collection.json` containing schema version 1
and a stable ID; collections without it continue to work locally. On first
access, path-keyed history is adopted into that stable identity transactionally.

Create a dedicated Supabase project and run `supabase_setup.sql` in its SQL
editor. Configure only the project URL in TOML:

```toml
[sync]
supabase_url = "https://your-project.supabase.co"
```

Export the server-side key as `PRACTICE_SUPABASE_KEY`. It must never be placed
in TOML. `PRACTICE_SUPABASE_URL` overrides the configured URL. The remote table
contains ratings, timestamps, compact compiler/reviewer metadata, and duration
fields; source, feedback bodies, review artifacts, cards, notes, sessions, and
diagnostics remain local.

For initial setup, synchronize the existing database on the one canonical
machine before adding another machine. A secondary machine should start with a
fresh SQLite database; its first sync downloads the ledger and reconstructs
cards. For machine-loss recovery, configure a fresh database and the same
collection/project. If both a legacy local database and the remote already have
history, sync reports `bootstrap_conflict` and changes neither ledger; use a
fresh database on that secondary machine.

Automatic sync runs asynchronously at editor startup, session start, and after
a rating. It never delays selection or replaces an open exercise. Use
`:PracticeSync` for an explicit result and `:PracticeDiagnostics` for configured
state, pending uploads, and last success. Network, authentication, paused-project,
rate-limit, malformed-response, or interrupted-process failures leave local
practice fully usable and retry on a later trigger. FSRS fuzzing stays enabled,
so historical statistics converge after synchronization while randomized due
dates and forecasts can differ slightly between machines.

## Tests

Run the script tests from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/scripts/tests -v
```

# Practice Workflow Scripts

This directory contains the editor-independent Python commands used by the
Neovim practice driver:

- `select_exercise.py` selects a due or unseen exercise from a collection.
- `evaluate_exercise.py` evaluates a submitted working copy.
- `record_rating.py` records the final rating and updates its FSRS card.
- `practice_scheduler.py` provides shared FSRS and SQLite behavior.

The commands communicate with callers through stable JSON input and output
contracts. Language-specific discovery and evaluation behavior belongs here,
while `src/nvim-driver` owns only Neovim workflow and presentation concerns.

Each command reads one JSON object from standard input and writes one JSON
object to standard output. A nonzero exit status means the command or request
failed. An exercise that does not compile is a successful evaluation command
whose `compiled` field is `false`.

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
`metadata_path`. The paths are absolute. The oldest due exercise is selected
first; when none is due, a random unseen exercise is selected. The previous
exercise is excluded when an equivalent alternative is available. When every
exercise has scheduling state and none is due, it returns `exercise: null` and
the UTC `next_due` timestamp.

`evaluate_exercise.py` accepts source and metadata paths plus a command array.
One or more arguments must contain the literal `{source}` placeholder. The
command is executed directly without a shell.

```json
{
  "source_path": "/temporary/working-copy.cpp",
  "metadata_path": "/collection/exercise.md",
  "command": ["g++", "-std=c++20", "-fsyntax-only", "{source}"]
}
```

It returns `compiled`, `diagnostics`, `metadata`, and `proposed_rating`. The
proposed rating is `good` for exit status zero and `fail` otherwise.

`record_rating.py` accepts:

```json
{
  "exercise_directory": "/collection/path",
  "exercise_id": "exercise-basename",
  "compiled": true,
  "proposed_rating": "good",
  "final_rating": "excellent",
  "database_path": "optional-database-override"
}
```

It maps `fail`, `acceptable`, `good`, and `excellent` to FSRS Again, Hard, Good,
and Easy. The updated card and immutable review log are committed together. A
successful response contains `recorded`, the next UTC `due` timestamp, and the
card `state`.

If `database_path` is omitted, both scheduler commands use
`PRACTICE_DATABASE`, then `$XDG_DATA_HOME/leetkatas/practice.sqlite3`, and
finally `~/.local/share/leetkatas/practice.sqlite3`.

## Tests

Run the script tests from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/scripts/tests -v
```

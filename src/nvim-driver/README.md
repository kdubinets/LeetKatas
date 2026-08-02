# Neovim Practice Driver

## Problem Statement

This project is a small, personal coding-practice environment built around
Neovim. Its purpose is to make short implementation-fluency exercises quick to
start, solve, review, rate, and repeat without leaving the editor.

The initial exercise collection is the C++20 core collection in
`practice/cpp/collections/core`. Each exercise currently consists of:

- A learner source file containing one `// Finish: ...` marker.
- A Markdown metadata file with the same basename containing the exercise name,
  description, and reference solution.

The original collection is read-only practice material. A practice session must
use a temporary working copy and must not modify the source exercise.

The Neovim component is a thin workflow driver over a set of Python scripts.
Selection, evaluation, and recording must remain usable independently of
Neovim. This separation will let the workflow and scheduling policy evolve
without coupling them to the editor UI.

The tool is intended for one user. It does not need anti-cheating measures,
multi-user isolation, or adversarial input handling.

## Running the Proof of Concept

From the repository root, launch the default C++ collection with:

```bash
src/nvim-driver/practice
```

Pass a different collection directory as the single optional argument:

```bash
src/nvim-driver/practice path/to/exercises
```

The launcher starts Neovim with its isolated configuration, without the normal
user configuration, and starts a practice session automatically. On first use,
it offers to install the pinned `which-key.nvim` v3.17.0 release into Neovim's
data directory for this isolated setup. After a short pause on a key prefix
(for example, Space or `z`), a popup shows the available continuations and their
descriptions. The cached plugin is used on subsequent launches.
`PRACTICE_PYTHON` may select a different Python executable and `CXX` may select
a different C++ compiler executable.

The driver requires Python 3.10 or newer and its pinned dependency:

```bash
python3 -m pip install -r src/nvim-driver/requirements.txt
```

`PRACTICE_DATABASE` may override the persistent SQLite database location.
`PRACTICE_NOTES_DIRECTORY` may override the directory used for personal
practice notes.

### User configuration

Personal practice defaults live in
`${XDG_CONFIG_HOME:-~/.config}/leetkatas/practice.toml`. Set `PRACTICE_CONFIG`
to load another file. The file is optional; an explicit collection argument or
environment variable takes precedence over it, and built-in defaults apply when
a setting is absent. `src/nvim-driver/practice.example.toml` is a copyable
starting point.

```toml
[practice]
collection = "~/work/LeetKatas/practice/cpp/collections/core"
# database_path = "~/.local/share/leetkatas/practice.sqlite3"
# log_path = "~/.local/state/nvim/leetkatas/practice.log"
# notes_directory = "~/.local/share/leetkatas/notes"
review_archive_ttl_days = 30

[reviewer]
model = "gpt-5.6-luna"
reasoning_effort = "low"

[editor]
indent_width = 4
which_key_delay_ms = 300

[evaluation]
compiler = "clang++"
```

Relative paths are resolved from the directory containing the configuration
file. The default collection is a user preference and belongs here; its
`environment.json` remains separate because it describes the language and
libraries against which submissions are evaluated.

Supported environment overrides include `PRACTICE_COLLECTION`,
`PRACTICE_DATABASE`, `PRACTICE_LOG`, `PRACTICE_NOTES_DIRECTORY`,
`PRACTICE_REVIEW_ARCHIVE_TTL_DAYS`, `PRACTICE_REVIEW_MODEL`,
`PRACTICE_REVIEW_EFFORT`, `PRACTICE_COMPILER`, and `CXX`. Passing a collection
directory to `src/nvim-driver/practice` has the highest precedence for the
collection. Review artifacts are retained for 30 days by default; set
`review_archive_ttl_days` to `0` to disable archiving or up to `3650` days to
change retention.

### Diagnostics and logs

The driver writes a structured JSON-lines diagnostic log to
`stdpath("state")/leetkatas/practice.log`. Set `PRACTICE_LOG` to override the
path. The log rotates to `practice.log.1` at 2 MiB and records session state,
notifications, subprocess commands, exit status, duration, stderr, and compact
response summaries. Reviewer summaries include the configured model and
reasoning effort. Exercise source, metadata bodies, and full reviewer responses
are not logged.

After a rating is recorded, the exact submitted source and complete structured
reviewer response are archived in the practice SQLite database. Expired
artifacts are deleted when the next rating is recorded, while compact review and
FSRS history remain. A database containing archived source is restricted to the
current user (`0600`).

Use `:PracticeDiagnostics` to show the current session ID, state, and log path.
Use `:PracticeLog` to open the log. When reporting a problem, the approximate
time or session ID is enough to correlate the relevant events.

## Long-Term Workflow

The intended complete loop is:

1. Select the next exercise.
2. Create and open a working copy in the main Neovim window.
3. Let the user complete the exercise without autocomplete or coding
   assistance, while retaining syntax highlighting.
4. Submit the working copy for evaluation.
5. Compile or otherwise validate it and ask an LLM to review it.
6. Present the evaluation, feedback, and a proposed rating.
7. Let the user accept or override the rating.
8. Record the final rating for future scheduling.
9. Select the next exercise and repeat.

The rating scale is:

| Value | Rating | Meaning |
|---:|---|---|
| 1 | Fail | Incorrect, incomplete, or not recalled. |
| 2 | Acceptable | Substantially correct, but difficult or notably weak. |
| 3 | Good | Correct with reasonable fluency. |
| 4 | Excellent | Correct, idiomatic, and recalled confidently. |

The numeric values intentionally mirror the convenient four-key rating flow of
spaced-repetition tools.

## Scope of the First Iteration

The first iteration was a proof of concept for the editor experience. Its goal
was to determine whether the solve, submit, review, rate, and continue cycle
felt fast and comfortable. The current implementation adds spaced repetition
but is not yet a complete correctness evaluator.

### Included

- Start a session for a specified exercise directory.
- Discover source and Markdown metadata pairs in that directory.
- Select an exercise randomly.
- Avoid immediately selecting the exercise that was just shown when more than
  one exercise is available.
- Create a session working copy, leaving the original exercise untouched.
- Open the working source in the main window and move the cursor to its practice
  marker.
- Keep syntax highlighting enabled.
- Disable autocomplete, LSP-driven assistance, snippets, AI assistance, and
  similar integrations in the dedicated practice setup.
- Submit the current working buffer through an editor command.
- Evaluate the submission by compiling it.
- Return and display compiler output together with the complete matching
  metadata file, including its reference solution.
- Propose `Good` after successful compilation and `Fail` after unsuccessful
  compilation.
- Allow the proposed rating to be overridden with any of the four ratings.
- Pass the final rating to a recording script.
- Implement the recording script as a no-op with a real command contract, so it
  can be replaced later without changing the editor.
- Continue to another randomly selected exercise.

The metadata is returned after every submission, including failed compilation,
so the user can always review the reference answer.

### Explicitly Deferred by the Proof of Concept

- LLM evaluation.
- Runtime or exercise-specific tests.
- Persistent attempt and rating history. Implemented in the FSRS iteration.
- Spaced-repetition scheduling. Implemented in the FSRS iteration.
- Retry behavior and other detailed failure flows.
- Support for Python or other languages.
- A general plugin installation and distribution story.
- Security and anti-cheating restrictions.

## Language-Independence Boundary

C++ is the only language configured in the first iteration, but the reusable
Neovim modules do not contain C++ compilation or file-format rules.

The editor should operate in terms of generic actions:

- `select`: choose an exercise and describe its files.
- `evaluate`: evaluate a submitted working file and return structured feedback.
- `record`: accept the final rating and attempt context.

Language-specific values are provided by the isolated entry-point profile and
optional collection `environment.json`. For the initial collection these are
the source extension, practice marker, C++20 compiler command, and structured
C++20 target environment. They are passed into generic workflow and script
interfaces as configuration. A later Python profile should be addable without
redesigning the Neovim workflow.

All script-facing results should use a stable JSON representation. Diagnostic
text intended for display should be a field in that representation rather than
being mixed with the protocol on standard output. Commands should return a
nonzero process status only when the command itself cannot complete; a learner
submission that fails to compile is a valid evaluation result.

## First-Iteration User Experience

### Start

`:PracticeStart {directory}` starts a session. The selector returns an exercise,
the driver creates a temporary working copy, and the main window opens it with
the cursor on the `Finish` marker.

The exercise source is the main solving interface. The metadata and reference
solution remain hidden until submission.

### Submit and review

`:PracticeSubmit` writes the current buffer and invokes the evaluator. Neovim
immediately opens a live evaluation pane with elapsed time and real progress
from the compiler and reviewer. It reports compilation completion, reviewer
attempts, and retry delays, then replaces itself with the final feedback.
The progress channel is a temporary JSON-lines file so the evaluator's stdout
remains reserved for its final protocol response. The pane becomes a dedicated
read-only `practice-feedback` buffer beside the source. Its opening view shows
the learner-facing outcome and proposed rating, concise reviewer summary, an
expanded correction for defective submissions, and grouped actions. A failed
compilation does not cap a positive reviewer rating; the feedback explains when
the reviewer recognized the approach despite the compiler result.

Detailed review evidence, non-empty compiler diagnostics, and the parsed
exercise reference follow lower in the buffer. Detailed review starts expanded
unless the proposed rating is `Excellent`; compiler details and the reference
start collapsed. Use `d`, `c`, and `r` to toggle them, or `?` for shortcut help. Structured
metadata is displayed without headings or fence delimiters; raw metadata is a
sanitized compatibility fallback. Extmark highlights distinguish outcomes,
ratings, actions, headings, hints, inline code, and code blocks.

This is an ordinary scratch buffer managed by the driver, not Neovim's special
preview window. That gives the driver predictable control over its contents,
focus, lifetime, and mappings. The buffer is not associated with a file, cannot
be modified, and is discarded when the user rates the attempt, skips, or quits.
Focus moves to it after evaluation so its rating shortcuts work immediately.

The wide feedback split targets 40% of the editor with a 52-column minimum
while preserving usable source space. Below 120 columns it uses a bottom split
at approximately 45% of the editor height.

Evaluation and rating calls are asynchronous so a future LLM call will not
freeze the editor.

### Capture personal notes

`:PracticeNote [kind]` opens a Markdown composer for the active exercise while
solving, evaluating, or reviewing. The optional kind is `follow-up` (the
default), `research`, or `exercise-fix`. `<Space>pm` captures the current line;
using it on a visual selection captures up to ten selected lines. Source notes
point back to the original exercise rather than its temporary working copy.
Feedback notes retain the current feedback section and a bounded excerpt.

Save with `:write` or `<C-s>`. A blank note is not written. Notes use readable,
chronological names such as
`2026-08-02-14-21-35--lower_bound_index.md`; a numeric suffix prevents an
existing file from being overwritten. Each file is independent, so notes may
be edited, moved, or deleted with ordinary filesystem tools.

The default directory is `${XDG_DATA_HOME:-~/.local/share}/leetkatas/notes`.
Configure `practice.notes_directory` or `PRACTICE_NOTES_DIRECTORY` to place it
elsewhere. `:PracticeNotes` or `<Space>po` edits that directory. An installed
directory handler can display it; otherwise the driver reports the absolute
path for use with another file manager or editor.

### Rate and continue

`:PracticeRate {rating}` records the selected rating and updates the exercise's
FSRS schedule. On success, the driver selects and opens the next due or unseen
exercise.

`:PracticeAccept` records the evaluator's proposed rating without requiring the
user to restate it, then selects and opens the next exercise.

`:PracticeRetry` closes feedback and returns to the unchanged working source
without recording a rating. The previous result remains in session memory only
until the next submission or exercise transition and is never archived.

`:PracticeNext` explicitly skips without changing scheduling state and selects
again from the scheduled queue.

`:PracticeQuit` ends the practice session and closes its temporary UI without
changing the original exercises.

Commands should reject actions that are invalid in the current state, such as
rating before submission, with a short explanatory message.

## Neovim Commands and Key Mappings

The dedicated Neovim setup must set the leader key to Space before registering
mappings:

```lua
vim.g.mapleader = " "
vim.g.maplocalleader = " "
```

Workflow mappings use the `p` prefix for practice:

| Mapping | Command | Purpose |
|---|---|---|
| `<Space>ps` | `:PracticeStart` | Start or restart a practice session. |
| `<Space>pc` | `:PracticeSubmit` | Check/submit the current solution. |
| `<Space>pa` | `:PracticeAccept` | Accept the proposed rating and continue. |
| `<Space>pr` | `:PracticeRetry` | Return to editing without recording. |
| `<Space>p1` | `:PracticeRate fail` | Record Fail and continue. |
| `<Space>p2` | `:PracticeRate acceptable` | Record Acceptable and continue. |
| `<Space>p3` | `:PracticeRate good` | Record Good and continue. |
| `<Space>p4` | `:PracticeRate excellent` | Record Excellent and continue. |
| `<Space>pn` | `:PracticeNext` | Skip and select again. |
| `<Space>pm` | `:PracticeNote` | Capture a note for the active exercise. |
| `<Space>po` | `:PracticeNotes` | Open the personal notes directory. |
| `<Space>pq` | `:PracticeQuit` | End the session. |

The numeric rating mappings should be displayed in the feedback UI so they do
not need to be memorized. The feedback UI should also display `<Space>pa` next
to the proposed rating as the fastest normal path. `PracticeStart` needs a way
to use a configured default directory when invoked from a mapping, since a
mapping cannot conveniently supply an arbitrary directory interactively. An
explicit command argument should override that default.

The workflow mappings are normal-mode mappings. The practice buffer should
make their purpose discoverable through mapping descriptions. Practice-only
mappings may be buffer-local, except for the start mapping, which must be
available before a practice buffer exists.

The feedback buffer additionally maps `a`, `1`–`4`, `n`, and `m` directly to
accept, rate, skip, and note. `d`, `c`, and `r` toggle detailed review, compiler
details, and the reference; `?` toggles shortcut help. `<CR>` accepts a correct
proposal, retries a defective result, or shows the manual-rating hint when no
proposal exists. All leader mappings remain available.

## Project Layout

```text
src/
├── nvim-driver/
│   ├── README.md
│   ├── init.lua                # isolated Neovim entry point
│   ├── practice                # launcher
│   └── lua/practice/
│       ├── init.lua            # setup, commands, and mappings
│       ├── session.lua         # state machine and working-copy lifecycle
│       ├── notes.lua           # per-file personal note composition
│       ├── process.lua         # Python subprocess/JSON adapter
│       └── ui.lua              # solving and feedback presentation
└── scripts/
    ├── practice_scheduler.py   # SQLite persistence and FSRS integration
    ├── select_exercise.py      # due-first/new-second selection
    ├── evaluate_exercise.py    # initial compiler-backed evaluator
    └── record_rating.py        # persistent FSRS review recording
```

Python owns the workflow operations and Lua owns editor state and presentation.

## Session State Model

The driver maintains an explicit small state machine. Selection and recording
are transitional states that prevent overlapping asynchronous commands:

```text
idle -> selecting -> solving -> evaluating -> reviewing -> recording
           ^          |              |                         |
           +-- next --+              +------ rate ------------+
           +---------------------------------------------------+
           +-- empty scheduled queue -> complete
```

- `idle`: no active exercise.
- `selecting`: the selector script is choosing the next exercise.
- `solving`: an exercise working copy is open.
- `evaluating`: a submitted copy is being checked.
- `reviewing`: feedback is visible and a rating can be chosen.
- `recording`: the final rating is being passed to the recorder.
- `complete`: all exercises have been introduced and none is currently due.

`PracticeNext` moves from `solving` or `reviewing` to a new `solving` state.
`PracticeRetry` moves from `reviewing` back to `solving` without changing the
working source or recording a rating; resubmission follows the normal path.
`PracticeQuit` returns a stable solving, reviewing, or complete state to `idle`. Commands
that would replace the session ask the user to wait while a script is running.

## Implementation

- The Python scripts implement paired-file discovery, FSRS due-first selection,
  configurable command evaluation, and transactional SQLite review history
  through JSON standard input/output.
- Lua owns temporary working copies, asynchronous process calls, the session
  state machine, editor commands, mappings, and feedback presentation.
- The isolated entry point supplies the initial C++ profile (`.cpp`, `.md`, the
  practice marker, and the C++20 GCC command); the reusable Lua modules contain
  no C++ parsing or compilation behavior.
- Python protocol tests live under `src/scripts/tests`, and the complete editor
  cycle is covered by `src/nvim-driver/tests/headless.lua`.

Run the automated checks from the repository root with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/scripts/tests -v
shellcheck src/nvim-driver/practice
PRACTICE_AUTOSTART=0 PRACTICE_DATABASE=/tmp/leetkatas-headless.sqlite3 \
  PRACTICE_NOTES_DIRECTORY=/tmp/leetkatas-headless-notes \
  nvim --headless --clean \
  -u src/nvim-driver/init.lua -l src/nvim-driver/tests/headless.lua
```

## Current Behavior

A session launched against the core C++ collection repeatedly completes this
loop without modifying the collection:

```text
due or ordered-unseen exercise -> edit -> submit -> see compile result and solution
                               -> choose/override rating -> scheduled next exercise
```

The loop is operable through the Space-leader mappings, retains syntax
highlighting, uses four-space indentation with spaces, provides no autocomplete
assistance, and invokes all three Python command boundaries. Progress and final
feedback panes color headings, successes, failures, warnings, and active work.
Due reviews take priority over unseen exercises; an empty
scheduled queue reports the next due time. A collection's `exercise_order.md`
controls unseen introductions with one exercise basename per line; collections
without one use random unseen selection.

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

Use `-s` (or `--sync-first`) when switching machines to finish Supabase
synchronization before the first exercise is selected:

```bash
src/nvim-driver/practice -s
```

The flag waits for one sync attempt, including reconstruction of downloaded
cards, then opens the first exercise. If synchronization is unavailable,
practice still opens using its local database.

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

### Problem-solving practice

Level C reasoning practice has a separate launcher and workspace:

```bash
src/nvim-driver/problem-solving
```

It presents a read-only problem brief, an optional hint, and a solution outline
that must be revealed before rating. Use `-s` to synchronize before initial
selection or pass a problem-solving collection as the optional argument. The
launcher uses the same pinned `which-key.nvim` shortcut assistant as Level A/B
and labels `<leader>p` as the problem-solving command group.

Its optional configuration lives at
`${XDG_CONFIG_HOME:-~/.config}/leetkatas/problem-solving.toml`; copy
`problem-solving.example.toml` as a starting point. The `[problem_solving]`
section accepts `collection`, `database_path`, `log_path`, `notes_directory`,
`supabase_url`, `private_content_sync`, and `retain_conversation_history`.
Environment overrides are
`PROBLEM_SOLVING_COLLECTION`, `PROBLEM_SOLVING_DATABASE`,
`PROBLEM_SOLVING_LOG`, `PROBLEM_SOLVING_NOTES_DIRECTORY`,
`PROBLEM_SOLVING_CONFIG`, `PROBLEM_SOLVING_SUPABASE_URL`, and
`PROBLEM_SOLVING_PRIVATE_CONTENT_SYNC`. Conversation configuration uses
`PROBLEM_SOLVING_RETAIN_CONVERSATION_HISTORY`, `PROBLEM_SOLVING_REVIEWER`,
`PROBLEM_SOLVING_REVIEWER_NAME`, `PROBLEM_SOLVING_REVIEW_MODEL`, and
`PROBLEM_SOLVING_REVIEW_EFFORT`. `PRACTICE_PYTHON` remains the shared Python
interpreter override.

Level C also uses the optional `[statusline]` table. Its recommended defaults
keep the information relevant to deliberate problem solving visible:

```toml
[statusline]
left = ["problem_name", "phase", "solve_elapsed"]
right = [
  "reviews_today", "new_today", "new_left", "reviews_total", "due_now",
  "due_later_today", "hint_requested", "outline_revealed", "bookmarked",
  "open_bookmarks", "action"
]
```

`solve_elapsed` runs only before the outline is revealed and freezes once the
discussion phase begins. The daily counters show reviews completed today, newly
reviewed problems today, due work now/later today, and unseen problems left;
`reviews_total` is the number of distinct problems reviewed in the collection.
The other Level C
items track hint/outline use, an open-thinking bookmark, outstanding bookmarks,
and the next available action. You can also use `problem_id`, `collection`, and
`conversation` (message count).

The primary mappings are `<leader>ph` for hint, `<leader>pr` for reveal,
`<leader>pg` for give-up and reveal, `<leader>pb` for bookmark, and
`<leader>pc` for clarification before reveal or solution discussion afterward.
`<leader>p1` through `<leader>p4` select Again, Hard, Good, and Easy after reveal.
Use `:ProblemSolvingBookmarks` to reopen the open-thinking queue and
`:ProblemSolvingDiagnostics` for local state and synchronization status.

Pre-reveal conversation receives only the public brief and may clarify wording
without giving strategy. After reveal, it can discuss the canonical outline.
Conversation history is retained locally by default and can be disabled with
`retain_conversation_history = false`; private Supabase synchronization remains
a separate explicit opt-in. Reviewer failures leave hint, reveal, rating, and
navigation actions available.

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
# follow_up_model = "gpt-5.6-terra"
# follow_up_reasoning_effort = "medium"

[editor]
indent_width = 4
which_key_delay_ms = 300
enhanced_syntax_highlighting = true

[statusline]
left = ["exercise_name"]
right = ["solve_elapsed", "time_today", "reviews_today", "due_now", "new_left"]
separator = " · "

[evaluation]
compiler = "clang++"

[sync]
# supabase_url = "https://your-project.supabase.co"
```

When an exercise opens, its import preamble is folded closed by default. This
currently recognises C/C++ `#include`, Python `import`/`from`, Rust `use`, and
common import forms for Go, JavaScript/TypeScript, Java, Kotlin, C#, Ruby, and
Swift. Use Neovim's normal fold commands (for example `zo` or `za`) to reveal
it. Support for a new exercise language is added in
`lua/practice/import_folds.lua` without changing the exercise UI.

Exercise source uses Tree-sitter syntax highlighting by default when Neovim has
the matching language parser installed. C++ practice still receives enhanced
semantic highlighting when no parser is available. Set
`editor.enhanced_syntax_highlighting = false` to use only the built-in rules.

The practice status line replaces the temporary working-copy filename with
exercise and scheduling context. Items are configured independently on the left
and right; an item that has no value in the current state is omitted together
with its separator. Set `statusline.enabled = false` to use Neovim's normal
status line.

Available items are:

- `exercise_name`, `exercise_id`, `collection`, and `language` for exercise context.
- `time_today`, `reviews_today`, `new_today`, and `new_left` for today's work and
  remaining unseen exercises. `time_today` includes the active exercise timer.
- `due_now`, `due_later_today`, and `tomorrow_due` for the current workload.
- `collection_progress` for an introduced/total summary such as `Seen 63/108`.
- `phase`, `phase_elapsed`, `solve_elapsed`, `progress`, and `action` for live
  workflow context. `solve_elapsed` runs only while solving, then remains fixed
  during evaluation and feedback.
- `compile_result` and `proposed_rating` for completed evaluation context.
- `modified` and `position` for conventional editor context.

For example, a workload-focused configuration can show every daily counter:

```toml
[statusline]
left = ["exercise_name", "language"]
right = [
  "time_today", "reviews_today", "due_now", "due_later_today",
  "new_today", "new_left"
]
separator = " | "
```

Relative paths are resolved from the directory containing the configuration
file. The default collection is a user preference and belongs here; its
`environment.json` remains separate because it describes the language and
libraries against which submissions are evaluated.

Supported environment overrides include `PRACTICE_COLLECTION`,
`PRACTICE_DATABASE`, `PRACTICE_LOG`, `PRACTICE_NOTES_DIRECTORY`,
`PRACTICE_REVIEW_ARCHIVE_TTL_DAYS`, `PRACTICE_REVIEW_MODEL`,
`PRACTICE_REVIEW_EFFORT`, `PRACTICE_FOLLOW_UP_MODEL`,
`PRACTICE_FOLLOW_UP_EFFORT`, `PRACTICE_FOLLOW_UP_REVIEWER`,
`PRACTICE_FOLLOW_UP_REVIEWER_NAME`, `PRACTICE_SUPABASE_URL`,
`PRACTICE_SUPABASE_KEY`, `PRACTICE_COMPILER`, and `CXX`. Passing a collection
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

Optional Supabase synchronization is documented in `../scripts/README.md`.
The key is read only from `PRACTICE_SUPABASE_KEY`; do not store it in TOML.
`:PracticeSync` reports explicit upload/download results, while automatic
attempts are silent and never block local practice.

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
start collapsed. Use `d`, `c`, and `r` to toggle them. Structured
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

### Ask the reviewer

While feedback is open, `?`, `:PracticeAsk [question]`, or `<Space>pf` asks the
reviewer a follow-up question. Omitting the command argument opens an input
prompt. Questions and answers appear with distinct styling in a Follow-up chat
section; `t` collapses or expands the conversation. Follow-up requests are
asynchronous, retain a bounded conversation history, and do not change the
original verdict or proposed rating.

Follow-up chat uses `reviewer.follow_up_model` and
`reviewer.follow_up_reasoning_effort` when configured, otherwise it inherits
the standard review settings. The equivalent environment overrides are
`PRACTICE_FOLLOW_UP_MODEL` and `PRACTICE_FOLLOW_UP_EFFORT`. Conversation turns
remain in session memory and are discarded when the learner retries, rates,
skips, or quits; they are not written to diagnostic logs or review artifacts.

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

Active learner time is stored with each completed review. Solve time accumulates
across retries, feedback-reading time runs while completed feedback is visible,
and both pause when Neovim loses focus or is suspended. Compiler, reviewer,
follow-up, and rating-process waits are excluded. Older reviews and skipped or
abandoned attempts have no tracked duration rather than a zero duration.

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

### Review statistics

`:PracticeStats [directory]` or `<Space>pt` opens a read-only statistics split.
It uses the active collection when a session exists, otherwise the configured
default; an explicit directory overrides both. Press `r` to refresh the snapshot
or `q` to close it without changing practice state.

The dashboard shows today's completed reviews, first-time introductions, rating
distribution, tracked time, due-now and later-today workload; current unseen,
Learning, Review (shown as Learned), and Relearning counts; the cards presently
scheduled tomorrow and across the next seven local calendar days; and a 30-day
daily history table. Due and forecast figures reflect current FSRS due dates and
do not simulate ratings that have not happened. Historical reviews of removed
exercises remain visible, while removed exercises are excluded from current
collection and forecast counts. Dates use the machine's local timezone; SQLite
timestamps remain UTC.

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
| `<Space>pf` | `:PracticeAsk` | Ask the reviewer a follow-up question. |
| `<Space>pi` | — | Toggle the current exercise's import/include preamble. |
| `<Space>po` | `:PracticeNotes` | Open the personal notes directory. |
| `<Space>pt` | `:PracticeStats` | Show current-collection statistics. |
| `<Space>pq` | `:PracticeQuit` | End the session. |

Within an active exercise buffer, `ZZ` submits the solution. In Insert mode,
`<C-Enter>` also submits and leaves Insert mode. While an evaluation (or another
practice operation) is pending, `ZZ` asks for confirmation before exiting
Neovim.

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
accept, rate, skip, and note. `d`, `c`, `r`, and `t` toggle detailed review,
compiler details, the reference, and follow-up chat; `?` asks the reviewer a
question. `<CR>` accepts a correct
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
    ├── review_follow_up.py     # bounded conversational reviewer bridge
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

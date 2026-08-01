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
user configuration or plugins, and starts a practice session automatically.
`PRACTICE_PYTHON` may select a different Python executable and `CXX` may select
a different C++ compiler executable.

The driver requires Python 3.10 or newer and its pinned dependency:

```bash
python3 -m pip install -r src/nvim-driver/requirements.txt
```

`PRACTICE_DATABASE` may override the persistent SQLite database location.

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

Language-specific values are provided by the isolated entry-point profile. For
the initial collection these are the source extension, practice marker, and
C++20 compiler command. They are passed into generic workflow and script
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
then opens a dedicated read-only feedback buffer in a vertical split to the
right of the source. The source remains visible in the main window so the
submitted code and reference answer can be compared side by side. The feedback
buffer presents:

- Whether compilation succeeded.
- Compiler diagnostics, when present.
- The exercise metadata and reference solution.
- The proposed rating.
- A clear prompt to accept or override the rating.

This is an ordinary scratch buffer managed by the driver, not Neovim's special
preview window. That gives the driver predictable control over its contents,
focus, lifetime, and mappings. The buffer is not associated with a file, cannot
be modified, and is discarded when the user rates the attempt, skips, or quits.
Focus moves to it after evaluation so its rating shortcuts work immediately.

The feedback split uses roughly one third of the editor width. When the editor
is narrower than 120 columns, it uses a bottom horizontal split instead.

Evaluation and rating calls are asynchronous so a future LLM call will not
freeze the editor.

### Rate and continue

`:PracticeRate {rating}` records the selected rating and updates the exercise's
FSRS schedule. On success, the driver selects and opens the next due or unseen
exercise.

`:PracticeAccept` records the evaluator's proposed rating without requiring the
user to restate it, then selects and opens the next exercise.

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
| `<Space>p1` | `:PracticeRate fail` | Record Fail and continue. |
| `<Space>p2` | `:PracticeRate acceptable` | Record Acceptable and continue. |
| `<Space>p3` | `:PracticeRate good` | Record Good and continue. |
| `<Space>p4` | `:PracticeRate excellent` | Record Excellent and continue. |
| `<Space>pn` | `:PracticeNext` | Skip and select again. |
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
  nvim --headless --clean \
  -u src/nvim-driver/init.lua -l src/nvim-driver/tests/headless.lua
```

## Current Behavior

A session launched against the core C++ collection repeatedly completes this
loop without modifying the collection:

```text
due or unseen exercise -> edit -> submit -> see compile result and solution
                       -> choose/override rating -> scheduled next exercise
```

The loop is operable through the Space-leader mappings, retains syntax
highlighting, provides no autocomplete assistance, and invokes all three Python
command boundaries. Due reviews take priority over unseen exercises; an empty
scheduled queue reports the next due time.

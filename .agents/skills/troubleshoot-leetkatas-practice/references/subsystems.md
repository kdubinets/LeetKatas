# Practice diagnostic map

| Boundary | Main files | Evidence |
|---|---|---|
| Launcher and environment | `src/nvim-driver/practice`, `src/nvim-driver/init.lua` | selected Python/compiler, startup notification, session log |
| Neovim process bridge | `lua/practice/process.lua`, `lua/practice/log.lua` | process start/finish, exit, stderr, decode error, duration |
| Session state and UI | `lua/practice/session.lua`, `lua/practice/ui.lua` | notifications, current state, evaluator validation, feedback rendering |
| Selection and scheduling | `select_exercise.py`, `practice_scheduler.py` | script response, SQLite errors, schema version, FSRS import |
| Compilation and review orchestration | `evaluate_exercise.py`, `reviewer_protocol.py` | compiler result, review status/failure/attempts |
| Codex adapter | `codex_reviewer.py` | preflight exit, Codex stderr, model override, schema errors |
| Persistence | `record_rating.py`, `practice_scheduler.py` | recorder response, transaction errors, review columns |

Default persistent log: Neovim `stdpath("state")/leetkatas/practice.log`.

Useful commands inside practice:

- `:PracticeDiagnostics` shows log path, session ID, and current state.
- `:PracticeLog` opens the JSONL log.

Environment controls:

- `PRACTICE_LOG`, `PRACTICE_PYTHON`, `PRACTICE_DATABASE`
- `PRACTICE_COMPILER`, `CXX`
- `PRACTICE_REVIEWER`, `PRACTICE_REVIEWER_NAME`
- `PRACTICE_CODEX`, `PRACTICE_REVIEW_MODEL`

# Problem-Solving Collections

This language-neutral practice area contains Level C reasoning cards. A card
presents a focused problem brief before reveal and keeps its hint, canonical
outline, provenance, and teaching metadata in a separate JSON record.

Collections live under `collections/`. Validate one by sending its path to the
Level C validator:

```bash
printf '%s\n' '{"collection_directory":"practice/problem_solving/collections/algorithmic_problem_solving"}' \
  | .venv/bin/python src/scripts/validate_level_c_collection.py
```

Launch the default collection in its dedicated read-only Neovim workspace:

```bash
src/nvim-driver/problem-solving
```

Pass a collection directory to override the configured default. The launcher
uses `${XDG_CONFIG_HOME:-~/.config}/leetkatas/problem-solving.toml` and the
`PROBLEM_SOLVING_` environment overrides documented in
[`src/nvim-driver/README.md`](../../src/nvim-driver/README.md).

See [`LevelCProblemSolvingFluency.md`](../../LevelCProblemSolvingFluency.md) for
the curriculum and file contract.

The Phase 2 JSON commands live in `src/scripts/`: select a card with
`select_problem_solving_card.py`, request hint/reveal state with
`problem_solving_card.py`, manage the open-thinking queue with
`problem_solving_bookmark.py`, persist the learner's self-rating with
`record_problem_solving_rating.py`, and inspect progress with
`problem_solving_stats.py`. `sync_problem_solving.py` backs up review and
bookmark events; private working artifacts synchronize only through an
explicit opt-in.

In Neovim, `:ProblemSolvingAsk` (or `<leader>pc`) clarifies wording before
reveal and discusses the canonical outline afterward. The clarification route
never receives hidden hint or solution content. Conversation history is kept
in the local card artifact by default; set `retain_conversation_history = false`
to keep it only for the current session. This local choice is independent from
the private-content synchronization opt-in.

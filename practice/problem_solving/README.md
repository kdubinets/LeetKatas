# Problem-Solving Collections

This language-neutral practice area contains Level C reasoning cards. A card
presents a focused problem brief before reveal and keeps its hint, canonical
outline, provenance, and teaching metadata in a separate JSON record.

Before preparing a new card, the
[candidate fit prompt](../../src/scripts/prompts/level_c_candidate_fit.txt)
asks whether the source leaves meaningful approach selection for the learner
and adds value to its collection. Its decision stays in the preparation report,
outside the published card schema.

Collections live under `collections/`. Validate one by sending its path to the
Level C validator:

```bash
printf '%s\n' '{"collection_directory":"practice/problem_solving/collections/medium_01"}' \
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

The difficulty-specific cohorts include
[`medium_01`](collections/medium_01/collection_spec.md),
[`medium_02`](collections/medium_02/collection_spec.md),
[`medium_03`](collections/medium_03/collection_spec.md),
[`medium_04`](collections/medium_04/collection_spec.md),
[`medium_05`](collections/medium_05/collection_spec.md),
[`medium_06`](collections/medium_06/collection_spec.md),
[`medium_07`](collections/medium_07/collection_spec.md),
[`medium_08`](collections/medium_08/collection_spec.md),
[`medium_09`](collections/medium_09/collection_spec.md), and
[`hard_01`](collections/hard_01/collection_spec.md). Launch any of them by
passing its directory. `medium_01` is the default. The nine medium cohorts
contain 225 cards in total; the 214 cards chosen by the seeded random draw and
all screened-out candidates are documented in the
[random-selection ledger](collections/medium_random_selection.json). Existing
statistics in the original mixed collection remain separate and do not affect
the new cohorts.

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

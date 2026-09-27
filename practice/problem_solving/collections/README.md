# Level C Collections

The [initial candidate fit review](CANDIDATE_FIT_REVIEW.md) evaluates the 16
original candidates against the Level C reasoning goal; 14 remain active.

- [`medium_01`](medium_01/collection_spec.md) contains the first medium cohort
  (25 cards: 11 earlier cards and 14 from the recorded random draw).
- [`medium_02`](medium_02/collection_spec.md) contains the second medium cohort
  (25 cards from the same draw).
- [`medium_03`](medium_03/collection_spec.md) and
  [`medium_04`](medium_04/collection_spec.md) contain the next 50 medium cards,
  each in a bounded 25-card cohort. Candidates were checked against all active
  medium cards and one another for substantial reasoning overlap.
- [`medium_05`](medium_05/collection_spec.md) and
  [`medium_06`](medium_06/collection_spec.md) contain another 50 medium cards
  in bounded 25-card cohorts. Candidates were checked against all 100 earlier
  medium cards and one another for substantial reasoning overlap.
- [`medium_07`](medium_07/collection_spec.md),
  [`medium_08`](medium_08/collection_spec.md), and
  [`medium_09`](medium_09/collection_spec.md) add 75 medium cards in three
  25-card cohorts, checked against the earlier 150 cards and one another.
- [`medium_random_selection.json`](medium_random_selection.json) records the
  reproducible candidate order, every reviewed decision, and both selected and
  filtered-out medium problems across all four random batches. Its source-quality
  rechecks track current canonical quality separately from Level C fit and
  overlap decisions. The 52 flagged explanations were repaired and independently
  reviewed as `canonical_explanation_bar_raised`; all five separately recorded
  statement issues are now resolved (`statement_and_canonical_review_passed`). The ten supporting-artifact findings are now
  resolved, and all 52 C++ harnesses passed address and undefined-behavior checks
  (leak detection was unavailable under environment process tracing). Quality
  passes cover the canonical explanations and C++; other languages were not tested.
  The local audit trail at `logs/problem-quality-audit.jsonl` preserves earlier
  failed reviews, raises, and current independent review records.
- [`hard_01`](hard_01/collection_spec.md) contains the first hard cohort
  (3 of 25 cards).
- [`algorithmic_problem_solving`](algorithmic_problem_solving/collection_spec.md)
  is the original mixed collection, retained as an archive. Its earlier
  practice history remains in the database but does not carry into the new
  cohorts.

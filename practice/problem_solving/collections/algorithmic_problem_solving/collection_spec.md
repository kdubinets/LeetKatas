# Algorithmic Problem-Solving Collection

## Status

Manually reviewed Level C foundation collection.

## Purpose and scope

This language-neutral collection trains unaided recognition, approach
selection, invariants, and correctness arguments. It began with the six
lowest-numbered problems in the repository's medium/hard bank that had a
canonical text solution: 2, 4, 8, 10, 15, and 23. It now also includes the
raised medium problems 47, 106, 199, 207, 216, 237, 306, 347, 375, and 445.

The set exercises linked-list simulation and arithmetic, partition binary
search, bounded parsing, sequence and interval dynamic programming,
backtracking, tree construction and traversal, graph feasibility, frequency
selection, sort-and-scan reasoning, and heap-based multiway merging. It is a
foundation corpus, not a claim of exhaustive problem-family coverage.

## Content boundary

Each `cards/<id>.brief.md` contains only a title and focused learner-visible
brief. Its paired `cards/<id>.card.json` contains source provenance, one hint,
the canonical outline, accepted alternatives, and teaching metadata. Cards are
language-neutral and contain no implementation code.

The canonical order is recorded in `problem_order.md`. Source hashes refer to
the exact local problem statements used during this conversion and allow the
validator to report stale cards after source edits.

## Validation

From the repository root:

```bash
printf '%s\n' '{"collection_directory":"practice/problem_solving/collections/algorithmic_problem_solving"}' \
  | .venv/bin/python src/scripts/validate_level_c_collection.py
```

Validation checks collection identity, exact card pairing and order coverage,
the version-1 schema, stable IDs, nonempty teaching fields, source provenance
and hashes, string-array metadata, and the public/private content boundary.

---
name: prepare-level-c-problem
description: Prepare, add, or review one numbered LeetKatas medium or hard problem as a language-neutral Level C reasoning card. Use when asked to convert a solved problem into a focused Level C brief, hint, canonical outline, provenance record, and collection entry, or to review such a card before publication. Require canonical text material, preserve source fidelity, prevent solution leakage, validate the collection, and leave final publication approval to a human.
---

# Prepare Level C Problem

Produce a draft reasoning card for unaided approach selection, not a coding
exercise or a condensed editorial.

## Inputs and boundaries

Require a difficulty (`medium` or `hard`), numeric problem ID, and target Level C
collection directory. Ask only for a missing input that cannot be inferred from
the request. Do not assume that the initial fixture collection should be
expanded.

Support two modes:

- **prepare/add/convert**: create or revise the requested draft card and update
  its collection order;
- **review/audit**: inspect and report findings without changing files unless
  the user explicitly asks to fix them.

Treat these as immutable source material:

```text
problems/<difficulty>/<id>.md
problems/<difficulty>/solutions/text/<id>.md
```

Write only the requested collection artifacts:

```text
<collection>/cards/problem-<id>.brief.md
<collection>/cards/problem-<id>.card.json
<collection>/problem_order.md
```

Never edit a source statement, starter, language solution, canonical text
solution, collection identity, or unrelated card. Do not create a missing
canonical solution as part of this workflow; report that prerequisite instead.

## Read before preparing

Read these files completely:

```text
LevelCProblemSolvingFluency.md
LevelCPromptDesign.md
src/scripts/prompts/level_c_problem_conversion.txt
<collection>/collection.json
<collection>/collection_spec.md
<collection>/problem_order.md
problems/<difficulty>/<id>.md
problems/<difficulty>/solutions/text/<id>.md
```

Inspect existing card records in the target collection for local tag,
prerequisite, fidelity-note, and ordering conventions. Read only enough existing
cards to establish those conventions; do not copy their problem-specific
content.

## Workflow

1. Confirm the source statement and canonical text solution exist. Read both in
   full and independently check that the canonical approach satisfies the
   statement, constraints, edge cases, and required complexity. Stop and report
   a source-material issue when an accurate card cannot be grounded safely.
2. Extract a private fidelity checklist before drafting: input/output semantics,
   distinctness and ordering rules, mutation or reuse rules, numeric bounds,
   approach-defining constraints, viable complexities, and material edge cases.
3. Apply `src/scripts/prompts/level_c_problem_conversion.txt`. Keep the brief
   language-neutral and learner-visible; keep the hint, outline, provenance,
   and teaching metadata private.
4. Use stable ID `problem-<id>`. Write the brief with exactly the source title as
   its first-level heading. Do not expose a source URL, attribution, tags, hint,
   outline, complexity target, or private teaching-field label in the brief.
5. Write a schema-version-1 card record with the exact fields documented in
   `LevelCProblemSolvingFluency.md`. Set `source.local_path` to the repository-
   relative source statement and calculate `source.content_sha256` from the
   exact bytes of that file. Do not hash the canonical solution.
6. Include exactly one nonempty hint and all six nonempty outline fields. Add an
   accepted alternative only after checking its correctness and complexity.
   Prefer the collection's established metadata vocabulary; use specific new
   terms when the problem genuinely adds a new family or prerequisite.
7. Review the public/private boundary and compare the draft against the fidelity
   checklist. Confirm that the brief is independently solvable, the hint is
   non-spoiling, the correctness argument supports the full contract, and the
   outline teaches reasoning without becoming an implementation walkthrough.
8. Add the ID exactly once to `problem_order.md`. Follow the ordering policy in
   the collection specification. If none is stated, preserve every existing
   entry, append the new ID, and disclose that assumption; never reorder the
   collection silently.
9. Run the Level C collection validator and `git diff --check`. Report the draft
   files, validation results, source or canonical-material concerns, fidelity
   judgments, and the requirement for human publication review.

## Existing cards and conflicts

If either card file already exists, inspect both paired files and the order
entry before acting. In prepare mode, do not overwrite an existing card unless
the user explicitly requests revision or correction. In review mode, classify
findings as `must_fix`, `should_improve`, or `optional`, citing the affected
artifact and concrete reason.

Preserve unrelated and untracked work. Do not treat generated problem files,
datasets, logs, or a dirty worktree as disposable.

## Validation

From the repository root, validate with the project virtual environment:

```bash
printf '%s\n' \
  '{"collection_directory":"<collection>","source_root":"."}' |
  .venv/bin/python src/scripts/validate_level_c_collection.py
```

The validator is necessary but not sufficient. Human review remains required
to approve source fidelity, hint disclosure, outline quality, and publication.

---
name: raise-leetkata-problem-quality
description: Audit or raise the educational quality of one existing LeetKatas problem or a bounded batch and its solution artifacts. Use when asked to audit, review quality, improve, or bar-raise numbered problems under problems, especially requests such as "audit medium 15", "raise medium 15 C++", or "bar-raise 50 unraised hard problems". Keep original problem statements and starter files read-only, improve only solution artifacts, and maintain a local audit trail to avoid redundant work.
---

# Raise LeetKatas Problem Quality

Use this skill to improve the quality of an existing teaching artifact, not to discover or catalogue patterns across problems.

## Modes and scope

Require a difficulty and numeric problem ID. `audit <difficulty> <id>` is read-only apart from its local audit log. `raise <difficulty> <id> <language>` may edit only the canonical explanation, named-language solution, and named-language tests below `problems/<difficulty>/solutions/`.

Treat these as immutable source material:

```text
problems/<difficulty>/<id>.md
problems/<difficulty>/<language>/<id>.<ext>
```

Never edit, rename, format, or otherwise modify source material. If it is defective or ambiguous, record the finding as a blocked external issue.

An audit examines the source statement plus every existing explanation, language solution, and test for the problem. A raise audits the same full set but changes only its named language and the shared explanation.

## Batch freshness and eligibility

For a request to raise a number of problems that have not been raised before, establish the batch before reviewing any candidate:

1. Capture a UTC `batch_started_at` boundary immediately, before selection or edits.
2. Build one exact list containing the requested number of unique problem IDs. Keep that list fixed unless an item proves ineligible or blocked; document any replacement.
3. Call `scripts/problem_quality_audit_log.py history --before <batch_started_at>` for the full list, repeating `--problem-id ID` for each candidate. An ID is eligible only when its pre-boundary `raise_count` is zero. A stale hash, recent file change, or lack of a current record does not override prior raise history.
4. Call `status` with every reviewed artifact for each eligible ID before its review. A prior audit-only record does not make the problem previously raised, but a current audit must still be deliberately superseded because the user's raise request is a forced review.

Never count an existing diff, passing test, current hash, or pre-boundary audit record as work completed for the new batch. Each selected ID counts only after its artifacts are actually reviewed, relevant findings are resolved, validation passes, and a new `mode=raise` record is appended with `audited_at >= batch_started_at`. An unchanged problem may count only when that new record documents a genuine post-boundary review.

Before claiming batch completion, run `history` twice for the fixed list:

- `--before <batch_started_at>` must report `raise_count=0` for every ID.
- `--not-before <batch_started_at>` must report at least one raise record for every ID.

Also rerun `status` for every candidate and require all hashes to be current. Verify the exact unique count rather than inferring completion from an ID range, timestamps alone, Git status, or the tail of the log. Report the exact IDs and changed-versus-unchanged counts.

## Audit trail

Keep the append-only, local-only audit trail at `logs/problem-quality-audit.jsonl`; it is intentionally Git-ignored. Before auditing, call `scripts/problem_quality_audit_log.py status` with every artifact to be reviewed. If the latest entry has identical hashes, report that the audit is current and stop unless the user explicitly requests a forced audit. If it is stale or absent, proceed and append a record after the audit or raise.

Record artifact paths and SHA-256 hashes, never artifact contents. Record the mode, scope, finding counts, outcome, changed solution paths, and validation results.

Counts alone do not preserve an audit. Put the concrete findings themselves into `--note` entries: what was flagged, in which artifact, its classification, and why anything classified `optional` was deliberately left unresolved. A later audit reads the notes to tell a genuinely clean artifact from one whose issues were merely deferred.

## Quality bar

Derive the expected solution independently from the source statement before trusting existing solution material. Assess:

1. Algorithmic correctness, complexity, edge cases, and output-order or mutation requirements.
2. Explanation accuracy, derivation, invariants or correctness argument, constraints, alternatives, and agreement with the code.
3. Idiomatic, clear target-language code that preserves the platform `Solution` interface; reject cleverness without teaching value.
4. Test coverage of examples, boundaries, likely wrong approaches, and important invariants. Treat tests as evidence rather than proof.

Classify every finding as `must_fix`, `should_improve`, or `optional`. Cite the artifact and the concrete reason. Do not add a pattern-library assessment.

## Raise and validate

For `raise`, make the smallest changes that resolve `must_fix` and worthwhile `should_improve` findings. Do not change unrelated languages. Preserve the existing solution unless a correction or clear teaching improvement is needed.

Run the relevant validator and tests after edits. For C++, use:

```bash
python3 .agents/skills/solve-leetkata-problem/scripts/verify_cpp_solution.py \
  problems/<difficulty>/solutions/cpp/<id>.cpp
```

Add `--test problems/<difficulty>/solutions/tests/cpp/<id>.cpp` when that harness exists. Run `git diff --check`, append the audit record, and report findings, changes, validation, and unresolved source-material issues.

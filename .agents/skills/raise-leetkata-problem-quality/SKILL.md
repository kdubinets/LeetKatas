---
name: raise-leetkata-problem-quality
description: Audit or raise the educational quality of one existing LeetKatas problem and its solution artifacts. Use when asked to audit, review quality, improve, or bar-raise a numbered problem under problems, especially requests such as "audit medium 15" or "raise medium 15 C++". Keep original problem statements and starter files read-only, improve only solution artifacts, and maintain a local audit trail to avoid redundant work.
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

## Audit trail

Keep the append-only, local-only audit trail at `logs/problem-quality-audit.jsonl`; it is intentionally Git-ignored. Before auditing, call `scripts/problem_quality_audit_log.py status` with every artifact to be reviewed. If the latest entry has identical hashes, report that the audit is current and stop unless the user explicitly requests a forced audit. If it is stale or absent, proceed and append a record after the audit or raise.

Record artifact paths and SHA-256 hashes, never artifact contents. Record the mode, scope, finding counts, outcome, changed solution paths, and validation results.

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

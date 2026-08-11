---
name: audit-cpp-interview-fluency
description: Audit whether LeetKatas Level A C++ implementation-fluency exercises adequately cover the reusable post-algorithm mechanics found in solved C++ interview problems. Use when asked to evaluate, benchmark, gap-analyze, or propose evidence-based Level A collection improvements from problems/medium or problems/hard; do not use to solve individual problems or generate exercises directly.
---

# Audit C++ Interview Fluency

Produce a read-only, reproducible coverage audit. The core collection trains atomic C++ implementation fluency, not algorithm discovery. Do not treat a missing algorithmic pattern as a Level A gap.

## Read first

Read, in order:

1. `practice/cpp/README.md`
2. `practice/cpp/collections/core/collection_spec.md`
3. `practice/cpp/collections/core/exercise_manifest.md`
4. Every `practice/cpp/collections/*/exercise_manifest.md`
5. `practice/cpp/InterviewFluencyAudit.md`

Use the core manifest to judge direct core coverage. Use every other manifest only to identify equivalent existing exercises and possible promotions; do not let specialised follow-up coverage make the core look complete.

## Select evidence

Audit only completed C++ solutions below `problems/<difficulty>/solutions/cpp/`. Exclude starter files, tests, and nonnumeric filenames.

Run the selector from the repository root. It consults the hash-aware audit ledger and selects only unchanged, unreviewed solutions. Its JSON output is the sample manifest and must be copied unchanged into the report.

```bash
python3 .agents/skills/audit-cpp-interview-fluency/scripts/select_solved_cpp_sample.py \
  --seed <recorded-seed> --medium-count 36 --hard-count 24 > /tmp/cpp-audit-sample.json
```

The ledger is `practice/cpp/audits/reviewed_solutions.json`. The selector stratifies each difficulty by numeric problem-ID range. It reports a shortfall rather than silently reusing unchanged solutions. A solution with changed contents becomes eligible again. Read each selected solution and its problem statement when available.

For a first audit, use one recorded seed. Before recommending a collection change, confirm every material candidate with a different recorded seed. For later corpus-growth audits, use a fresh recorded seed and retain prior reports.

## Classify mechanics

For each solution, ignore the algorithm-discovery step. Record only reusable implementation actions needed once the approach is known. Map each action to exactly one status:

| Status | Meaning |
|---|---|
| `core` | Directly trained by a core exercise. |
| `partial` | The core trains a meaningful component but not the whole atomic action. |
| `follow_up` | Taught by an existing non-core collection only. |
| `candidate` | Absent everywhere, atomic, reusable, and plausibly one minute or less. |
| `out_of_scope` | Algorithmic pattern, problem-specific construction, or a task too broad for Level A. |

Name the evidence precisely: solution path, mechanic, and matching manifest exercise(s). Do not count generic syntax, ordinary loops, or a variable declaration as gaps unless the recurring action itself needs deliberate fluency practice.

Classify a candidate as a recommendation only when it recurs across at least three distinct sampled solutions, has a clear single primary objective, and is not a near-duplicate of an exercise in any collection. Treat a `follow_up` candidate as a promotion decision, not a new-exercise proposal.

## Report and handoff

Create one report under `practice/cpp/audits/` using the format in `practice/cpp/InterviewFluencyAudit.md`. Include the seed, script JSON, source counts, selected paths, per-solution evidence, aggregate coverage, rejected non-gaps, and recommendations. After completing the report, record the reviewed sample:

```bash
python3 .agents/skills/audit-cpp-interview-fluency/scripts/record_audited_solutions.py \
  --manifest /tmp/cpp-audit-sample.json \
  --report practice/cpp/audits/YYYY-MM-DD-<short-name>.md \
  --recorded-at YYYY-MM-DD
```

Do not record a sample that was not actually reviewed. The ledger stores the report path and source hash, not the classification; reports remain the evidence trail.

Keep the audit read-only. Do not add, rename, edit, or validate exercise pairs unless the user explicitly asks to act on accepted recommendations. If asked to generate exercises later, first read the relevant collection specification and use the normal collection workflow.

## Verification

Before handoff:

1. Re-run the selector with the same arguments before recording and confirm identical JSON.
2. Record the completed sample, then confirm its paths are no longer eligible unless their contents change.
3. Check every report path and manifest reference.
4. Run `git diff --check`.

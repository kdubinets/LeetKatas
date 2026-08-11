# C++ Interview-Fluency Audits

Use an audit to decide whether the Level A core collection trains the small, reusable C++ mechanics that appear after an interview problem's algorithm is already understood. An audit evaluates the collection; it does not change it.

## When to run one

Run an initial audit before expanding the core collection from interview evidence. Run another after the solved medium/hard corpus grows materially, or when a prior audit leaves an important borderline recommendation unresolved.

Do not audit every solution at once. A bounded, stratified sample is more useful than a corpus-wide count because it keeps review practical and stops frequently occurring generic code from dominating the conclusions. Audits accumulate: unchanged solutions are normally reviewed once, then excluded from later samples.

## Recommended configuration

Use a strong coding/reasoning model. As a default, use GPT-5.6 Terra with high reasoning effort for routine audits. Use GPT-5.6 Sol with high reasoning effort for final synthesis or borderline classifications. Reserve xhigh or max for designing the audit process or resolving a difficult dispute, rather than for every sampled solution.

## Runbook

1. Use `$audit-cpp-interview-fluency`.
2. Choose and record an integer seed.
3. Generate a sample from solved C++ solutions:

   ```bash
   python3 .agents/skills/audit-cpp-interview-fluency/scripts/select_solved_cpp_sample.py \
     --seed 20260809 --medium-count 36 --hard-count 24 > /tmp/cpp-audit-sample.json
   ```

4. Inspect each selected solution and its statement when present.
5. Record only mechanics required after choosing the algorithm, then map them to the core and follow-up manifests.
6. Save the report as `practice/cpp/audits/YYYY-MM-DD-<short-name>.md`.
7. Record the completed sample in the ledger:

   ```bash
   python3 .agents/skills/audit-cpp-interview-fluency/scripts/record_audited_solutions.py \
     --manifest /tmp/cpp-audit-sample.json \
     --report practice/cpp/audits/YYYY-MM-DD-<short-name>.md \
     --recorded-at YYYY-MM-DD
   ```

8. Confirm any material proposal on a second, differently seeded sample before changing a collection.

The selector searches only `problems/<difficulty>/solutions/cpp/`, so it excludes learner starter files and test harnesses. It stratifies by numeric problem-ID range within each difficulty. Before recording, re-running it with identical arguments must produce identical JSON.

## Review ledger

`practice/cpp/audits/reviewed_solutions.json` is the machine-readable inventory of reviewed evidence. It stores each solution path, its current content hash, and the report/date that reviewed that version. It does not replace reports or contain the audit's reasoning.

By default, the selector excludes solutions whose current hash already appears in the ledger. A changed solution automatically becomes eligible again. If an ID stratum has too few eligible solutions, the selector reports a shortfall instead of reusing old evidence.

Re-review an unchanged solution only deliberately: to resolve a disputed classification, assess a changed audit rule/model, or verify a material proposed change. Prefer a second unseen sample for normal confirmation.

## How to interpret coverage

| Result | Meaning | Action |
|---|---|---|
| Core coverage | A core exercise directly trains the action. | No change. |
| Partial coverage | Core trains part, but not all, of the atomic action. | Track; recommend only if recurrence shows a real gap. |
| Follow-up coverage | A non-core collection teaches it. | Decide whether it belongs in core; do not duplicate automatically. |
| Candidate gap | It is absent everywhere and is a small reusable action. | Require recurrence and confirmation. |
| Out of scope | It is an algorithmic pattern or too broad for Level A. | Record as evidence for a future idiom/pattern track. |

A candidate merits a Level A proposal only when it appears in at least three distinct sampled solutions, has one clear primary implementation objective, remains normally solvable in about a minute, and is not essentially duplicated anywhere in the collections.

## Seed policy

A seed makes an audit reproducible: a later reviewer can inspect the exact evidence behind a conclusion. A different seed tests whether that conclusion generalizes. The ledger makes a fresh seed broaden coverage rather than randomly revisit the same unchanged files. Keep all previous reports; do not overwrite a report merely because a newer sample reaches a different conclusion.

Use one recorded seed for exploratory audits. Use a second recorded seed to confirm changes that would add or promote exercises. When the corpus grows, use a fresh seed and compare its findings with the audit history.

## Report template

```markdown
# Audit: <short name>

## Scope

- Date: YYYY-MM-DD
- Auditor: <model and reasoning effort>
- Collection evaluated: `collections/core`
- Purpose: <initial, confirmation, or corpus-growth audit>

## Sample manifest

```json
<unchanged selector output>
```

## Per-solution evidence

| Solution | Post-algorithm mechanic | Status | Existing exercise evidence | Notes |
|---|---|---|---|---|

## Aggregate findings

| Mechanic | Status | Distinct solutions | Evidence | Decision |
|---|---|---:|---|---|

## Rejected non-gaps

| Finding | Reason |
|---|---|

## Recommendations

State only confirmed proposals. For each, name the atomic objective, recurrence evidence, equivalent follow-up coverage if any, and why it belongs in core. State explicitly when no changes are justified.

## Verification

- [ ] Re-ran selector with identical arguments and got identical JSON.
- [ ] Recorded this completed sample in `reviewed_solutions.json`.
- [ ] Confirmed recorded, unchanged solutions are no longer eligible.
- [ ] Checked all cited manifest and solution paths.
- [ ] Ran `git diff --check`.
```

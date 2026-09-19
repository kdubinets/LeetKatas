# Dynamic Programming State Idioms

## Status

Active, provisional Level B collection designed from general considerations at the user's request. No LeetCode corpus was parsed. It is not corpus-audited, complete, or frozen.

The collection contains ten exercise pairs in three conceptual batches, with a ten-entry manifest and canonical order.

## Language and Level

Up-to-C++20, using only the standard library. Each exercise supplies the state meaning, recurrence or transition, base cases, and dependency order in the Pattern hint. The learner implements one state-storage or dependency-maintenance idiom, normally in 3–8 minutes.

These exercises do not ask the learner to recognize that dynamic programming applies, invent a state, derive a recurrence, select an iteration order, or independently choose a space optimization.

## Task Descriptions and Hints

Each learner source has exactly one result-focused `// Finish:` comment. It states the observable result, input preconditions, and boundary behavior without prescribing the algorithm. It remains understandable without the hidden hint.

One `// Pattern:` comment supplies the dynamic-programming model and invariant without giving code or standard-library APIs. A blank line after it lets the practice driver hide it independently of imports. Reveal or hide it with `<Space>h` or `:PracticeHint`.

Metadata has only Name, Description, and Solution. Description records the supplied recurrence and implementation skill, but introduces no behavioral requirement absent from the source.

## Included State Shapes

- Two scalar states for a supplied one-dimensional recurrence.
- One rolling row whose current cells depend on current-row and prior-row state.
- Descending in-place capacity updates for zero-one choices.
- Ascending in-place amount updates for reusable choices.
- In-place two-sequence rows with a saved prior diagonal.
- Top-down memoization whose cache distinguishes an uncomputed state from a valid zero.
- Minimization with an explicit unreachable-state sentinel.
- Coupled finite-state transitions derived from one prior snapshot.
- Aggregation over a variable set of predecessor states.
- Rotation of distinct previous and current rows with bounded neighbor dependencies.

The zero-one and reusable-choice exercises deliberately form a contrast: their opposite update directions enforce different reuse rules. The rolling-row exercises remain distinct because one has a grid boundary invariant while the other must preserve an overwritten diagonal dependency.

## Reassessment

The initial six exercises covered rolling scalars and rows, opposite zero-one/reusable update orders, a saved diagonal, and explicit memo state. Reassessment retained four additions with new state mechanics: unreachable minimization, coupled-state snapshots, aggregation over variable predecessor sets, and rotation of separate rows. Fibonacci/tiling variants, edit distance, subset-sum stories, and obstacle-grid paths were rejected as repetitions of existing invariants; interval DP remains outside this introductory collection.

## Excluded Topics

- Discovering DP state, recurrence, base cases, dependency order, or optimization.
- Multi-pattern full problems, multidimensional domain modelling, interval DP, digit DP, tree DP, bitmask DP, and advanced optimization.
- Reconstructing a solution path until it demonstrates a distinct bounded Level B invariant.
- Separate exercises that only change a story, value type, or number of dimensions.
- Calling an atomic standard-library algorithm already covered by Level A.

## Verification

From `practice/cpp/`:

```bash
tools/validate_exercises.sh collections/b_level/dynamic_programming_state_idioms c++20
../../.venv/bin/python tools/test_dynamic_programming_state_idioms.py
```

The runtime tool substitutes recorded solutions in temporary source, compiles with sanitizers, and compares deterministic exhaustive and seeded inputs with independent reference implementations. It never completes learner files in place. Runtime verification is authoring validation rather than a new practice-driver stage.

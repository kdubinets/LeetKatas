# Level B C++ Interview Implementation Idioms

## Purpose

Level B is the bridge between Level A atomic C++ implementation fluency and full interview-problem practice. A Level B exercise gives the learner the algorithmic idiom to implement; the learner practises recalling and maintaining its standard state, invariant, and control flow.

It does not ask the learner to discover an algorithm, combine several independently selected patterns, or solve a complete LeetCode problem unaided.

## Exercise contract

- One named, reusable interview implementation idiom.
- One primary state-management or invariant-maintenance objective.
- Normally 3–8 minutes of learner-written code.
- Exactly one `// Finish:` section and the normal paired `.cpp` / `.md` format.
- The learner source explicitly names the pattern and its invariant, without revealing exact APIs or code.
- Metadata keeps `# Name`, `# Description`, and `# Solution`; its description names the pattern, invariant, inputs, constraints, and implementation skill.
- One canonical exercise per idiom by default. Add a variation only when it changes the state shape, invariant, or primary implementation decision.

Example source guidance:

```cpp
// Pattern: sliding window. Keep the current window valid by shrinking its left edge.
// Finish: return the greatest valid window length
```

## Development route

1. Create a Level B core collection from established, reusable idioms.
2. Extend the library through focused follow-up collections, each organized around one state-model family.
3. Mine solved medium and hard C++ interview solutions for recurring patterns and gaps, using a dedicated Level B audit workflow and cumulative evidence ledger.

Generate the core in small, reviewable batches. Validate it against real solutions before declaring it complete or frozen. The existing Level A audit is not the right tool: it deliberately excludes the larger idioms that Level B is intended to cover.

## Initial core proposal

Start with `collections/sequence_scanning_and_window_idioms/`, targeting roughly 16–24 exercises. Its scope is sequential stateful scans, not every interview pattern.

Strong candidate families:

- fixed-size rolling windows;
- shrink-to-valid sliding windows with an explicit invariant;
- two pointers that converge or move in lockstep;
- slow/fast pointers for in-place sequence compaction;
- frequency-table maintenance during a scan;
- prefix sums and prefix-frequency state;
- difference-array range updates;
- manual binary-search loop variants.

Monotonic stacks may join this collection only if the manifest remains coherent; otherwise they begin the next focused collection.

## Roadmap after the initial core

Create a collection only when enough non-duplicate exercises share its state model. Candidate families are:

1. Monotonic stacks and ordered-boundary searches.
2. Trees and recursive state propagation.
3. Graph traversal state and visitation discipline.
4. Linked-list pointer rewiring.
5. Intervals, heaps, and event scheduling.
6. Disjoint sets and connectivity bookkeeping.

This is a roadmap, not a quota. Leave a family unbuilt if it produces only weak variants or belongs more naturally in normal problem practice.

## Application integration

The existing Neovim driver can launch and schedule a Level B collection without UI changes. Give each collection a stable `collection.json`, C++20 `environment.json`, manifest, and canonical `exercise_order.md`.

Begin with the current compile-and-review workflow. Add deterministic runtime test support later when several Level B exercises demonstrate a clear need for it; it is a reliability enhancement, not a prerequisite or a replacement for reviewer feedback.

## Evidence and tools

Use `$develop-cpp-level-b-idioms` for planning, creating, or reviewing Level B collections. Use GPT-5.6 Terra with high reasoning effort as the default; reserve Sol for difficult boundary judgments or final audits.

After the initial core exists, add a separate Level B audit skill. It should use seeded, stratified, unseen-first samples of solved C++ medium and hard solutions, a hash-aware ledger distinct from the Level A ledger, and explicit classifications for trained idioms, partial coverage, candidate gaps, duplicate variations, and out-of-scope algorithm discovery.


---
name: solve-leetkata-problem
description: Create, review, or extend a LeetKatas solution for one numbered LeetCode problem in a requested difficulty and language. Use when asked to solve, add, explain, validate, test, or review a numbered problem under problems, especially requests such as "solve medium 15 in C++" or "review medium 15 in C++". Create the canonical teaching explanation when missing, preserve existing language solutions, and produce clear idiomatic code plus deterministic verification.
---

# Solve LeetKatas Problem

Treat each completed solution as a teaching artifact for reusable interview and language patterns, not merely an accepted submission.

## Inputs and layout

Require a difficulty, numeric problem ID, and one target language. Ask for only the missing input. Support `cpp`, `python`, and `rust` when their starter file exists.

Read these files before editing:

```text
problems/<difficulty>/<id>.md
problems/<difficulty>/<language>/<id>.<ext>
problems/<difficulty>/solutions/text/<id>.md       (if present)
problems/<difficulty>/solutions/<language>/<id>.<ext> (if present)
```

Write completed artifacts only below:

```text
problems/<difficulty>/solutions/text/<id>.md
problems/<difficulty>/solutions/<language>/<id>.<ext>
problems/<difficulty>/solutions/tests/<language>/<id>.<ext>
```

Do not overwrite an existing target-language solution or test unless the user explicitly asks to revise it. Report its presence and validate it instead. Never alter the original statement or starter file merely to add a solution.

## Workflow

1. Confirm the requested problem and starter exist. Read the statement, constraints, and examples in full.
2. If an explanation exists, independently check its algorithm, complexity, invariants, and edge cases against the statement. Correct it when it is wrong or materially incomplete; state the correction in the handoff.
3. If no explanation exists, create it. Include the recognition cues, selected approach, correctness reasoning, complexity, edge cases, alternatives and their trade-offs, and named reusable patterns. Add language-specific notes only when they teach a meaningful idiom.
4. Create only the requested language solution. Preserve the platform's `Solution` interface and write an idiomatic, readable implementation appropriate to its standard library.
5. Prefer the clearest expert implementation. Keep short, commented-out alternatives near the relevant code only when they demonstrate a reusable language idiom or a material trade-off. Explain why the alternative may be chosen; never add alternatives as decoration.
6. Run the language validator. When the request includes testing, add a language-specific runtime harness and run it. Read `references/cpp-testing.md` for C++ conventions.
7. Run `git diff --check` and report created/updated files, validation, and any limitations in the statement or tests.

## Explanation quality

Explain how to derive the solution, not just its final form. Name the algorithmic pattern and the invariant that makes it correct. Mention viable alternatives only when their trade-off teaches something useful. Keep the canonical explanation language-independent; put target-language idioms in a clearly labelled language-notes section.

## Optional adversarial review

When asked to `review <difficulty> <id> <language>`, do not create a new solution. Independently derive the expected algorithm from the statement, then inspect the existing explanation, target-language solution, and test harness if present. Check correctness, complexity, edge cases, explanation-to-code consistency, target-language idioms, and whether the tests could expose likely mistakes. Run available deterministic validation.

Report findings by severity and cite the affected artifact. A review is read-only: do not change files unless the user asks to `review and fix`. In that mode, correct only the reviewed explanation, target-language solution, or its test harness, then rerun validation.

## Verification

For C++, run:

```bash
python3 .agents/skills/solve-leetkata-problem/scripts/verify_cpp_solution.py \
  problems/<difficulty>/solutions/cpp/<id>.cpp
```

Run the same command with `--test problems/<difficulty>/solutions/tests/cpp/<id>.cpp` when a C++ harness exists. The test harness must cover examples, boundary cases, and cases aimed at common errors or the implementation's key invariant. Treat AI-generated tests as evidence, not proof; use a small brute-force oracle or property checks for algorithms where that is practical.

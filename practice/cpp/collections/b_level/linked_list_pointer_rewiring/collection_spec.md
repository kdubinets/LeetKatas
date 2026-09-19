# Linked-List Pointer Rewiring

## Status

Active, provisional Level B collection designed from general considerations at the user's request. No LeetCode corpus was parsed. It is not corpus-audited, complete, or frozen.

The collection contains six exercise pairs, generated and reviewed in two batches of three, with a six-entry manifest and canonical order.

## Language and Level

Up-to-C++20, using only the standard library. Each exercise trains a supplied interview implementation idiom and one primary link invariant, normally in 3–8 minutes. This is not algorithm discovery or an implementation of a complete linked-list container.

## Node and Ownership Contract

Every learner file supplies the same singly linked `Node` model: an integer value and a nullable `next` pointer. Inputs are finite, acyclic, null-terminated chains; two merge inputs are disjoint. The caller owns and keeps every node alive.

Functions may change links and the returned head, but must not allocate or delete list nodes, change values, or replace existing nodes with copies. Constant auxiliary space includes the call stack; a fixed number of local sentinel nodes is permitted. Removed nodes remain caller-owned and their links are unspecified.

These requirements must be visible in each learner source, not merely in this specification or hidden metadata. A short essential block comment states the shared input, ownership, and space constraints; this keeps Finish readable without concealing constraints in the hint.

## Task Descriptions and Hints

Each source has exactly one `// Finish:` comment describing the required result, constraints, and boundary behavior without implementation steps or APIs. It must be understandable independently of the hint.

One `// Pattern:` comment names the supplied pointer strategy and invariant without revealing assignments or code. A blank line after it lets the practice driver fold it closed independently of imports. Reveal or hide it with `<Space>h` or `:PracticeHint`.

Metadata has only the standard Name, Description, and Solution sections; every behavioral requirement in Description must already be visible in the source. The solution contains only the replacement for Finish.

## Inventory and Order

The provisional six-idiom scope is whole-list reversal, predecessor-based filtering, tail-based sorted merging, two-chain stable partitioning, adjacent-pair swapping, and bounded segment reversal. Generate in two batches of three and review the manifest after each batch; do not add weak variants to meet a quota.

Whole-list reversal trains preservation of an unprocessed suffix. Segment reversal adds preservation and reconnection of both outer boundaries. Array scans and merges do not train maintaining node topology or null termination. Level A list API exercises delegate rewiring to a container and are not duplicates of these tasks.

## Reassessment

The first batch covered whole-chain reversal, filtering, and sorted merging. Reassessment retained stable two-chain partitioning, adjacent-pair blocks, and bounded segment reversal because they add distinct tail termination, repeated local reconnection, and outer-boundary invariants. Individual insertion/deletion, traversal-only pointer problems, and compound reorder/sort problems were rejected as too small, owned elsewhere, or multi-idiom.

## Excluded Topics

- Individual insertion or deletion at a supplied node: generally too small for Level B.
- Middle finding, cycle detection, and intersection finding: primarily traversal.
- List sorting, palindrome checking, arbitrary group reversal, and full reorder-list problems: multi-idiom combinations.
- Random-pointer cloning, ownership design, allocation, and complete list classes.
- Doubly linked operations until a separate bidirectional invariant justifies an extension.

## Verification

From `practice/cpp/`:

```bash
tools/validate_exercises.sh collections/b_level/linked_list_pointer_rewiring c++20
../../.venv/bin/python tools/test_linked_list_pointer_rewiring.py
```

Runtime checks must substitute the recorded solutions without editing learner files and compare exact node identities and order, unchanged values, and null termination. Cover empty and singleton inputs, consecutive and complete removal, equal merge keys, empty partition groups, odd pair counts, and segments touching either end. Bounded traversal catches extra nodes and cycles without hanging.

Runtime verification is authoring validation, not a new practice-driver evaluation stage. A future dedicated Level B audit may assess prevalence and gaps; this collection makes no corpus coverage claim.

The runtime tool requires Python 3 and a C++20 compiler (g++ by default, or CXX). It uses AddressSanitizer and UndefinedBehaviorSanitizer with leak detection disabled because the exercise contract forbids allocation and ptrace sandboxes cannot run LeakSanitizer. It uses deterministic exhaustive short inputs and seeded longer inputs, keeps generated source and binaries temporary, and never completes learner files in place.

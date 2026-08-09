# C++ Exercise Collections

This directory contains focused C++ practice collections and the documentation used to grow and validate them.

## Layout

```text
cpp/
├── AGENTS.md
├── README.md
├── CppFollowUpTopics.md
├── CppProblemsGenerationPrompt.md
├── collections/
│   ├── README.md
│   ├── core/
│   │   ├── collection.json
│   │   ├── collection_spec.md
│   │   ├── environment.json
│   │   ├── exercise_manifest.md
│   │   ├── exercise_order.md
│   │   └── 108 exercise pairs
│   ├── non_owning_views_and_ranges/
│   │   └── 30 exercise pairs plus collection metadata
│   ├── ownership_move_semantics_and_raii/
│   │   └── 36 exercise pairs plus collection metadata
│   ├── templates_and_concepts/
│   │   └── 36 exercise pairs plus collection metadata
│   ├── text_processing_and_conversion/
│   │   └── 28 exercise pairs plus collection metadata
│   ├── numeric_and_bit_manipulation/
│   │   └── 26 exercise pairs plus collection metadata
│   ├── variants_and_error_modelling/
│   │   └── 21 exercise pairs plus collection metadata
│   ├── custom_value_types_and_comparisons/
│   │   └── 21 exercise pairs plus collection metadata
│   ├── callable_utilities/
│   │   └── 20 exercise pairs plus collection metadata
│   ├── chrono/
│   │   └── 36 exercise pairs plus collection metadata
│   ├── filesystem/
│   │   └── 37 exercise pairs plus collection metadata
│   └── cpp20_language_features/
│       └── 15 exercise pairs plus collection metadata
└── tools/
    └── validate_exercises.sh
```

## Current Collections

The [core collection](collections/core/collection_spec.md) contains 108 Level A implementation-fluency exercises targeting idiomatic C++ up to and including C++20. It is considered complete and should normally remain frozen.

Eleven focused up-to-C++20 follow-up collections are also complete:

- [Non-Owning Views and Ranges](collections/non_owning_views_and_ranges/collection_spec.md) contains 30 exercises on spans, string views, lazy composition, iterator/sentinel ranges, borrowing, and materialization.
- [Ownership, Move Semantics, and RAII](collections/ownership_move_semantics_and_raii/collection_spec.md) contains 36 exercises on smart pointers, ownership transfer, moved-from states, rule-of-zero composition, move-aware handles, and deterministic cleanup.
- [Templates and Concepts](collections/templates_and_concepts/collection_spec.md) contains 36 exercises on template forms, dependent names, packs, traits, compile-time branching, requires-expressions, named concepts, and constrained overloads.
- [Text Processing and Conversion](collections/text_processing_and_conversion/collection_spec.md) contains 28 exercises on character conversion, streams, regular-expression APIs, and C++20 formatting.
- [Numeric and Bit Manipulation](collections/numeric_and_bit_manipulation/collection_spec.md) contains 26 exercises on bit utilities, masks, safe numeric operations, reductions, and randomization.
- [Variants and Error Modelling](collections/variants_and_error_modelling/collection_spec.md) contains 21 exercises on variant state handling and visitation, optional composition, explicit value-or-error results, and error boundaries.
- [Custom Value Types and Comparisons](collections/custom_value_types_and_comparisons/collection_spec.md) contains 21 exercises on equality, three-way comparison categories, ordered key policies, heterogeneous lookup, and hashing contracts.
- [Callable Utilities](collections/callable_utilities/collection_spec.md) contains 20 exercises on type-erased callbacks, overload selection, uniform invocation, binding, reference wrappers, callable adaptors, and C++20 lambda forms.
- [Chrono](collections/chrono/collection_spec.md) contains 36 exercises on durations, time points, deadlines, civil calendars, calendar differences, weekdays, and time-of-day decomposition.
- [Filesystem](collections/filesystem/collection_spec.md) contains 37 exercises on lexical paths, status and mutation operations, error-code overloads, symbolic links, recursive copying, and directory traversal.
- [C++20 Language Features](collections/cpp20_language_features/collection_spec.md) contains 15 language-delta exercises on initialization, scoped names, conditional explicitness, lambda changes, UTF-8 types, attributes, and variadic preprocessing.

The core [exercise order](collections/core/exercise_order.md) records the canonical
1-to-108 progression as one exercise basename per line. The
[exercise manifest](collections/core/exercise_manifest.md) records generation
batch, primary implementation skill, and supporting topics.

## Planning Documents

- [Follow-up topics](CppFollowUpTopics.md) lists proposed up-to-C++20 collections and a separate C++23-delta curriculum.
- The [base generation prompt](CppProblemsGenerationPrompt.md) defines the exercise-pair format and general quality requirements.

## Validation

Validate the collections from this directory with:

```bash
tools/validate_exercises.sh collections/core c++20
tools/validate_exercises.sh collections/non_owning_views_and_ranges c++20
tools/validate_exercises.sh collections/ownership_move_semantics_and_raii c++20
tools/validate_exercises.sh collections/templates_and_concepts c++20
tools/validate_exercises.sh collections/text_processing_and_conversion c++20
tools/validate_exercises.sh collections/numeric_and_bit_manipulation c++20
tools/validate_exercises.sh collections/variants_and_error_modelling c++20
tools/validate_exercises.sh collections/custom_value_types_and_comparisons c++20
tools/validate_exercises.sh collections/callable_utilities c++20
tools/validate_exercises.sh collections/chrono c++20
tools/validate_exercises.sh collections/filesystem c++20
tools/validate_exercises.sh collections/cpp20_language_features c++20
```

The validator compiles temporary completed forms through a pipe; it does not modify learner files or leave generated solutions in the repository.

## Adding a Collection

1. Create `collections/<descriptive_name>/`.
2. Write `collection_spec.md` before generating exercises.
3. Add `collection.json` with a stable, globally unique ID when progress should be portable or syncable.
4. Add `environment.json` when the evaluation harness should receive explicit target-language, library, or tool restrictions.
5. Create `exercise_manifest.md` and treat it as the collection inventory.
6. Add `exercise_order.md` when the collection has a canonical introduction order.
7. Generate and validate exercises in reviewable batches.
8. Reassess gaps after each batch and freeze the collection when only weak variants remain.

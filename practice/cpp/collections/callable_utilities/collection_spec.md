# Callable Utilities

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 20 Level A exercises.
- 20 `.cpp` learner files and 20 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from type erasure through invocation and binding to reference adaptation and lambda forms.

## Language Boundary

This is an up-to-C++20 collection. It targets callable facilities and lambda forms available in C++20 and does not use C++23 move-only function wrappers, back binding, or forwarding-like utilities.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train practical construction, storage, invocation, adaptation, and lifetime-aware use of callable objects without turning the exercises into algorithm-design problems.

## Included Topics

- Type-erased callbacks, overloaded-function selection, empty callback states, ordered callback execution, and retained callable state with `std::function`.
- Uniform invocation of member functions, member data, and arbitrary forwarded callables with `std::invoke`.
- Leading-argument and member-function binding with `std::bind_front`.
- Mutable and const reference adaptation with `std::reference_wrapper`, `std::ref`, and `std::cref`.
- Member-function adaptation and predicate negation with `std::mem_fn` and `std::not_fn`.
- Generic lambdas, explicit lambda template parameter lists, and move-only initialized captures.

## Excluded Topics

- Ordinary predicate lambdas, projections, mutable generation lambdas, overloaded variant visitors, and tuple application already covered by existing collections.
- Perfect-forwarding theory, variadic folds, concepts, and other template-language topics beyond the small invocation wrapper included here.
- Legacy `std::bind`, deprecated function adaptors, C++23 `std::move_only_function`, `std::bind_back`, and `std::forward_like`.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/callable_utilities c++20
```

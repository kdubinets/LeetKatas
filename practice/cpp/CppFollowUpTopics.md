# C++ Follow-Up Exercise Collections

## Scope

The existing implementation-fluency collection targets idiomatic C++ up to and including C++20. The follow-up collections below should use the same interpretation unless a collection explicitly names a newer standard.

The C++23 section is different: it is a delta curriculum. It should target facilities introduced in C++23 on top of the existing C++20 material, rather than repeating fundamentals inherited from earlier standards.

## Collection Size Estimates

The estimates below assume atomic, high-quality implementation-fluency exercises
of the same approximately one-minute Level A scope as the completed core
collection. They exclude skills that are already substantially covered by core.
The recommended target is a planning point rather than a quota; stop within the
stated range when only duplicate, trivial, or overly exotic candidates remain.

## Up-to-C++20 Follow-Up Collections

### 1. Non-Owning Views and Ranges

Recommended target: 28 exercises (sensible range: 24–32).

Progress: complete with [30 validated exercises](collections/non_owning_views_and_ranges/collection_spec.md).

- `std::span`, including fixed and dynamic extents.
- Deeper `std::string_view` slicing and parsing.
- Range-view composition and lazy evaluation.
- Iterator and sentinel differences.
- Borrowed ranges, dangling iterators, and lifetime safety.
- Materializing views into owning containers in C++20.

### 2. Ownership, Move Semantics, and RAII

Recommended target: 32 exercises (sensible range: 28–36).

Progress: complete with [36 validated exercises](collections/ownership_move_semantics_and_raii/collection_spec.md).

- `std::unique_ptr`, `std::shared_ptr`, and `std::weak_ptr`.
- Ownership transfer and observing without taking ownership.
- Moved-from states and correct use of `std::move`.
- Rule of zero and small move-aware value types.
- Deterministic cleanup and scope-based resource ownership.
- Wrapping non-memory resources in RAII types.

### 3. Templates and Concepts

Recommended target: 30 exercises (sensible range: 26–34).

- Function and class templates.
- Variadic templates and fold expressions.
- Type traits and `if constexpr`.
- C++20 concepts and requires-expressions.
- Constrained overloads and abbreviated function templates.
- Forwarding references and perfect forwarding.

### 4. Variants and Error Modelling

Recommended target: 20 exercises (sensible range: 18–24).

- Inspecting and extracting `std::variant` alternatives.
- `std::visit` and overloaded visitors.
- More advanced `std::optional` composition.
- Explicit success-or-error result structures.
- Exception boundaries and translating failures into values.

### 5. Custom Value Types and Comparisons

Recommended target: 22 exercises (sensible range: 18–26).

- Equality and relational operators.
- C++20 three-way comparison and defaulted comparisons.
- Defining strict weak orderings for custom types.
- Custom hashing and equality for unordered containers.
- Safely using custom types as map and set keys.

### 6. Concurrency

Recommended target: 18 exercises (sensible range: 14–22).

- `std::thread` and `std::jthread`.
- Stop tokens and cooperative cancellation.
- `std::mutex`, `std::lock_guard`, `std::unique_lock`, and `std::scoped_lock`.
- Condition variables and predicate waits.
- Atomic values and basic memory-order awareness.
- C++20 latches, barriers, and semaphores.
- Safe task input and result handoff.

### 7. Text Processing and Conversion

Recommended target: 18 exercises (sensible range: 15–21).

Progress: complete with [28 validated exercises](collections/text_processing_and_conversion/collection_spec.md).

- Allocation-aware parsing with `std::string_view`.
- `std::from_chars` and `std::to_chars`.
- Tokenization without unnecessary allocation.
- Stream extraction and formatting.
- C++20 `std::format`, where the selected standard library supports it.

### 8. Numeric and Bit Manipulation

Recommended target: 20 exercises (sensible range: 17–24).

Progress: complete with [26 validated exercises](collections/numeric_and_bit_manipulation/collection_spec.md).

- `<bit>` utilities and `std::bitset`.
- Bit masks, flags, and safe unsigned operations.
- Numeric conversions and overflow awareness.
- Reductions, scans, interpolation, and rounding.
- Random engines and distributions.

### 9. Callable Utilities

Recommended target: 16 exercises (sensible range: 13–20).

- `std::function` and type-erased callbacks.
- `std::invoke` and member pointers.
- `std::bind_front`.
- `std::reference_wrapper`.
- Stateful, generic, and template lambdas.

### 10. Compile-Time Programming

Recommended target: 17 exercises (sensible range: 14–20).

- `constexpr` functions and standard-library operations.
- `consteval` and `constinit`.
- Compile-time validation with `static_assert`.
- Template lambdas and compile-time branching.
- Distinguishing compile-time capability from mandatory compile-time evaluation.

### 11. Chrono

Recommended target: 18 exercises (sensible range: 15–22).

- Duration arithmetic and explicit duration conversion.
- Time-point comparison and elapsed-time calculations.
- Duration rounding.
- Deadlines and timeout calculations.
- C++20 calendar and time-zone facilities where available.

### 12. Filesystem

Recommended target: 14 exercises (sensible range: 12–17).

- Constructing and joining paths.
- Extracting filenames, stems, and extensions.
- File status and existence checks.
- Directory iteration.
- Exception-based versus `std::error_code` overloads.

### 13. C++20 Language Features

Recommended target: 12 exercises (sensible range: 10–15).

- Designated initializers.
- Initialized range-for statements.
- `using enum`.
- Template parameter lists on lambdas.
- Conditional `explicit`.
- Aggregate and structured-binding patterns.

### 14. Coroutines

No Level A collection is recommended: even introductory exercises need
non-trivial supporting coroutine types and do not naturally meet the one-minute
implementation-fluency constraint. If a longer Level B collection is explicitly
defined, target 8 exercises (sensible range: 6–10).

- Coroutine vocabulary and execution flow.
- Suspension and resumption.
- Coroutine-frame lifetime.
- Small generator-like types.
- Basic awaitable and promise types.

Coroutines should be treated as an advanced collection. Even introductory exercises require more supporting code than the one-minute implementation-fluency format.

## C++23 Delta Collections

These topics should assume fluency with the existing up-to-C++20 exercises and test only the new C++23 capability or the new implementation pattern it enables.

### Priority 1: Strong Practical Targets

#### 1. `std::expected`

Recommended target: 22 exercises (sensible range: 18–26).

- Constructing success and error states.
- Reading values and errors safely.
- Returning `std::expected<void, E>`.
- Chaining with `and_then`, `transform`, `or_else`, and `transform_error`.
- Converting exception-style or sentinel-style APIs into explicit results.

#### 2. Monadic `std::optional`

Recommended target: 12 exercises (sensible range: 10–14).

- Chaining optional-producing operations with `and_then`.
- Transforming contained values.
- Supplying lazy alternatives with `or_else`.
- Avoiding nested conditionals when composing optional operations.

#### 3. C++23 Ranges Materialization and Folds

Recommended target: 12 exercises (sensible range: 10–15).

- Materializing views with `std::ranges::to`.
- Left and right folds.
- Folds without an explicit initial value.
- Retaining the final iterator when using fold-with-iterator forms.

#### 4. C++23 Range Algorithms

Recommended target: 16 exercises (sensible range: 13–19).

- `contains` and `contains_subrange`.
- `starts_with` and `ends_with` for arbitrary ranges.
- `find_last`, `find_last_if`, and `find_last_if_not`.
- Range versions of `iota`, `shift_left`, and `shift_right`.

#### 5. C++23 Range Views

Recommended target: 28 exercises (sensible range: 23–34).

- `zip` and `zip_transform` for parallel traversal.
- `enumerate` for indexed traversal.
- `adjacent` and `adjacent_transform` for neighboring elements.
- `chunk`, `chunk_by`, `slide`, and `stride`.
- `join_with` for flattened ranges with separators.
- `cartesian_product` for direct product traversal.
- `repeat`, `as_const`, and `as_rvalue`.
- Writing a reusable adaptor with `std::ranges::range_adaptor_closure`.

#### 6. Formatted Output and Range Formatting

Recommended target: 11 exercises (sensible range: 8–14).

- `std::print` and `std::println`.
- Formatting containers and ranges.
- Formatting tuples and escaped/debug strings.
- Choosing compile-time format strings versus runtime format strings.

#### 7. `std::mdspan`

Recommended target: 14 exercises (sensible range: 11–17).

- Constructing multidimensional non-owning views.
- Accessing two- and three-dimensional data.
- Static versus dynamic extents.
- Layout mappings and strides.
- Passing multidimensional data without copying.

#### 8. Flat Associative Containers

Recommended target: 13 exercises (sensible range: 10–16).

- `std::flat_map`, `std::flat_multimap`, `std::flat_set`, and `std::flat_multiset`.
- Lookup and insertion behavior.
- Sorted-storage implications.
- Choosing flat containers versus node-based associative containers.

#### 9. `std::generator`

Recommended target: 8 exercises (sensible range: 6–10).

- Consuming a generator as a range.
- Yielding values from a coroutine.
- Yielding references safely.
- Understanding generator lifetime and laziness.

#### 10. Move-Only Callables and Callable Utilities

Recommended target: 10 exercises (sensible range: 8–13).

- `std::move_only_function` with move-only captures.
- Passing and storing move-only callbacks.
- `std::bind_back`.
- Applying cv/ref qualification with `std::forward_like`.

### Priority 2: Focused C++23 Collections

#### 11. C++23 String and Stream Facilities

Recommended target: 8 exercises (sensible range: 6–10).

- `std::string::contains` and `std::string_view::contains`.
- `resize_and_overwrite` for direct buffer population.
- `std::spanstream` for stream operations over existing buffers.

#### 12. Lifetime and C Interoperability Utilities

Recommended target: 5 exercises (sensible range: 4–7).

- `std::out_ptr` and `std::inout_ptr` for C-style output parameters.
- `std::start_lifetime_as` for explicitly beginning object lifetime in storage.
- Exercises should use small, well-defined wrappers and avoid unsafe raw-storage puzzles.

#### 13. Small C++23 Utilities

Recommended target: 7 exercises (sensible range: 5–9).

- `std::byteswap`.
- `std::to_underlying`.
- `std::unreachable`, limited to preconditions already enforced by the surrounding code.
- Size-type literal suffixes `z` and `uz`.

#### 14. Diagnostics

Recommended target: 4 exercises (sensible range: 3–6).

- Capturing and storing `std::stacktrace`.
- Formatting or printing stack traces.
- Keeping stacktrace exercises observational rather than dependent on exact platform output.

### Priority 3: C++23 Language Delta

#### 15. Explicit Object Parameters

Recommended target: 6 exercises (sensible range: 4–8).

- Deducing `this` for shared const and non-const implementations.
- Recursive lambdas without external type erasure.
- Preserving value category with explicit object parameters.
- Reducing duplicated overload sets.

#### 16. Constant-Evaluation Improvements

Recommended target: 8 exercises (sensible range: 6–10).

- `if consteval`.
- C++23's relaxed `constexpr` function restrictions.
- Separating immediate and runtime behavior cleanly.

#### 17. New Operator Forms

Recommended target: 7 exercises (sensible range: 5–9).

- Multidimensional `operator[]`.
- Static `operator()` and static `operator[]`.
- Captureless static lambdas.

#### 18. Explicit Decay Copy and Implicit Move

- `auto(expression)` and `auto{expression}` as explicit decay-copy operations.
- C++23's simpler implicit move rules for local return values and parameters.
- Exercises must make ownership and value-category consequences observable.

#### 19. Additional Language Features

- `[[assume]]`, only when the precondition is already guaranteed.
- `#elifdef` and `#elifndef` in small configuration exercises.
- Extended floating-point types where the compiler provides them.

### Toolchain-Sensitive C++23 Topics

- Standard-library modules `std` and `std.compat`.
- `std::stacktrace` symbol quality.
- `std::print`, range formatting, `std::generator`, and `std::mdspan` availability.
- Extended floating-point types.

Before generating exercises for these topics, check the compiler and standard-library feature-test macros. Do not replace a missing standard facility with a vendor extension while still labeling the exercise as portable C++23.

## Recommended Collection Order

1. Non-owning views and ranges, up to C++20.
2. Ownership, move semantics, and RAII, up to C++20.
3. Templates and concepts, up to C++20.
4. Variants and error modelling, up to C++20.
5. C++23 `expected`, optional monadic operations, ranges, and formatted output.
6. C++23 `mdspan`, flat containers, generators, and move-only callables.
7. Concurrency.
8. Focused language-delta and toolchain-sensitive collections.

## Standards References

- [WG21 feature-test macro recommendations](https://isocpp.org/std/standing-documents/sd-6-sg10-feature-test-recommendations)
- [WG21 C++23 ranges plan](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2214r2.html)
- [WG21 library plan for completing C++23](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2489r0.html)
- [WG21 library evolution report covering generators, modules, and mdspan](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2400r3.html)
- [WG21 committee paper index](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/)

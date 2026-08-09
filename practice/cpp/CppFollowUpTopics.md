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

Progress: complete with [36 validated exercises](collections/templates_and_concepts/collection_spec.md).

- Function and class templates.
- Variadic templates and fold expressions.
- Type traits and `if constexpr`.
- C++20 concepts and requires-expressions.
- Constrained overloads and abbreviated function templates.
- Forwarding references and perfect forwarding.

### 4. Variants and Error Modelling

Recommended target: 20 exercises (sensible range: 18–24).

Progress: complete with [21 validated exercises](collections/variants_and_error_modelling/collection_spec.md).

- Inspecting and extracting `std::variant` alternatives.
- `std::visit` and overloaded visitors.
- More advanced `std::optional` composition.
- Explicit success-or-error result structures.
- Exception boundaries and translating failures into values.

### 5. Custom Value Types and Comparisons

Recommended target: 22 exercises (sensible range: 18–26).

Progress: complete with [21 validated exercises](collections/custom_value_types_and_comparisons/collection_spec.md).

- Equality and relational operators.
- C++20 three-way comparison and defaulted comparisons.
- Defining strict weak orderings for custom types.
- Custom hashing and equality for unordered containers.
- Safely using custom types as map and set keys.

### 6. Concurrency

Recommended target: 18 exercises (sensible range: 14–22).

Progress: complete with [37 validated exercises](collections/concurrency/collection_spec.md).

- `std::thread` and `std::jthread`.
- Stop tokens and cooperative cancellation.
- `std::mutex`, `std::lock_guard`, `std::unique_lock`, and `std::scoped_lock`.
- Condition variables and predicate waits.
- Atomic values and basic memory-order awareness.
- Atomic shared-ownership publication and consumption.
- C++20 latches, barriers, and semaphores.
- Safe task input and result handoff.
- Non-interleaved output with `std::osyncstream`.

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

Progress: complete with [20 validated exercises](collections/callable_utilities/collection_spec.md).

- `std::function` and type-erased callbacks.
- `std::invoke` and member pointers.
- `std::bind_front`.
- `std::reference_wrapper`.
- Stateful, generic, and template lambdas.

### 10. Compile-Time Programming

Recommended target: 17 exercises (sensible range: 14–20).

Progress: complete with [18 validated exercises](collections/compile_time_programming/collection_spec.md).

- `constexpr` functions and standard-library operations.
- `consteval` and `constinit`.
- Compile-time validation with `static_assert`.
- Immediate lambdas and evaluation-context-dependent branching.
- Distinguishing compile-time capability from mandatory compile-time evaluation.

### 11. Chrono

Recommended target: 18 exercises (sensible range: 15–22).

Progress: complete with [36 validated exercises](collections/chrono/collection_spec.md).

- Duration arithmetic and explicit duration conversion.
- Time-point comparison and elapsed-time calculations.
- Duration rounding.
- Deadlines and timeout calculations.
- C++20 calendar and time-zone facilities where available.

### 12. Filesystem

Recommended target: 14 exercises (sensible range: 12–17).

Progress: complete with [37 validated exercises](collections/filesystem/collection_spec.md).

- Constructing and joining paths.
- Extracting filenames, stems, and extensions.
- File status and existence checks.
- Directory iteration.
- Exception-based versus `std::error_code` overloads.

### 13. C++20 Language Features

Recommended target: 12 exercises (sensible range: 10–15).

Progress: complete with [15 validated exercises](collections/cpp20_language_features/collection_spec.md).

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

## Additional Up-to-C++20 Coverage Gaps

This section records gaps found by comparing the current exercise inventory with
the C++ language and standard-library areas documented by cppreference and the
WG21 C++20 change summary. It supplements the collection roadmap above without
changing the scope or status of any existing collection.

The purpose is not exhaustive standard-library enumeration. Future work should
select practical, transferable implementation skills that fit the established
Level A format: one clear objective, normally about one minute of learner-written
code, minimal supporting machinery, and no algorithm-discovery requirement.

### Priority 1: Core Language Mechanics

#### 1. Class Interfaces, Special Members, and Operator Overloading

Current ownership exercises cover rule-of-zero storage, move-only declarations,
one custom move constructor, one custom move-assignment operator, and resource
cleanup in a destructor. Comparison operators are covered deeply by the custom
value-types collection. General class-interface and operator fluency remains
sparse.

Strong exercise families include:

- Constructor member-initializer lists and initialization of base subobjects.
- Delegating constructors and inherited constructors where they simplify a small
  interface.
- Defaulting or deleting individual special member functions deliberately.
- Implementing a copy constructor for a small independently owned value.
- Implementing copy assignment, including a focused copy-and-swap form when the
  supplied type makes that the natural implementation.
- Marking move construction and move assignment `noexcept` when their operations
  cannot throw.
- Recognizing how a user-declared destructor or copy operation affects implicit
  move generation, expressed through declarations rather than language-lawyer
  questions.
- Pure virtual functions, abstract interfaces, `override`, `final`, and a
  defaulted virtual destructor.
- Bringing a hidden base-class overload into a derived class with a
  using-declaration.
- Safe pointer-form `dynamic_cast` when a polymorphic interface is already
  supplied.
- Explicit conversion operators such as `operator bool` for small wrapper types.
- Prefix increment or decrement that mutates and returns the updated object by
  reference.
- Postfix increment or decrement that preserves and returns the previous value.
- Compound assignment operators and symmetric binary operators implemented in
  terms of them.
- Const and non-const subscript overloads for a supplied wrapper.
- Dereference and arrow operators for a small handle-like or iterator-like type.
- A function-call operator for a small stateful function object.
- Stream insertion and extraction operators when the I/O behavior is already
  specified and remains atomic.

Keep each operator conventional. Do not ask learners to invent surprising
semantics, implement a complete iterator or smart pointer, or write an entire
rule-of-five type in one exercise.

#### 2. Type Deduction and Value Categories

Template argument deduction and class template argument deduction are covered,
but ordinary `auto` and `decltype` choices are mostly incidental rather than
primary learner objectives.

Strong exercise families include:

- Use `auto` when an intentional value copy is required.
- Use `auto&` or `const auto&` to retain reference semantics and avoid a copy.
- Use `auto&&` where forwarding or binding to a range result is the intended
  behavior.
- Demonstrate that plain `auto` drops top-level references and cv-qualification
  through an observable, non-puzzle task.
- Use `decltype(name)` to reproduce a declared type.
- Distinguish `decltype(expression)` from `decltype((expression))` where reference
  preservation has a practical consequence.
- Return `decltype(auto)` from a small forwarding accessor so a reference result
  is preserved.
- Use a trailing return type when the result type depends on function parameters.
- Choose value versus reference structured bindings intentionally.
- Mutate tuple-like or map elements through a reference structured binding.
- Use `std::type_identity_t` to place one function parameter in a non-deduced
  context when another parameter should control the type.

Avoid isolated deduction quizzes. Every exercise should make the ownership,
copying, mutability, or return-type consequence visible in the surrounding code.

#### 3. Initialization

The C++20 language-delta collection covers designated and parenthesized aggregate
initialization, but general initialization forms are not systematically trained.

Strong exercise families include:

- Value-initialize a scalar or aggregate with braces when a known zero or empty
  state is required.
- Avoid an indeterminate scalar caused by default initialization.
- Use list initialization where rejecting narrowing is part of the contract.
- Distinguish direct initialization from copy initialization when an `explicit`
  constructor is involved.
- Initialize data members directly in a constructor's member-initializer list.
- Use a default member initializer unless a constructor supplies an override.
- Delegate from one constructor to another rather than duplicate initialization.
- Initialize a base-class subobject with the required constructor arguments.
- Respect declaration-order initialization when members depend on one another.
- Construct an optional, variant alternative, pair, tuple, or container element
  in place when direct construction is the actual skill.
- Initialize references only where the owner and required lifetime are explicit.
- Use `std::initializer_list` only for a practical range-like interface or one
  carefully chosen overload-resolution case.

Do not build a collection from brace-initialization traps or undefined reads.
The preferred exercises produce correct initialization rather than ask learners
to predict surprising behavior.

#### 4. Name Resolution, Visibility, and Practical Overload Selection

Existing exercises touch `using enum`, dependent-name disambiguation, hidden
friend comparisons, and selecting an overloaded function for storage. Namespace
lookup, argument-dependent lookup, base-class hiding, and common overload choices
remain largely uncovered.

Strong exercise families include:

- Qualify a name to select the intended namespace member.
- Import one specific name with a using-declaration.
- Define or use a short namespace alias for a supplied deeply nested namespace.
- Use the customization pattern `using std::swap; swap(left, right);`.
- Invoke a supplied hidden friend through argument-dependent lookup.
- Restore base-class overloads hidden by a derived declaration.
- Distinguish name hiding from virtual overriding in a small supplied hierarchy.
- Select const versus non-const member overloads through the correct object type.
- Select lvalue- versus rvalue-reference overloads through the correct value
  category.
- Explicitly select one free-function overload when a callable object or function
  pointer requires a single signature.
- Place a symmetric operator or conversion in the correct member or non-member
  location so ordinary conversions work on both operands.

Avoid ambiguous-program puzzles, broad using-directives, obscure two-phase lookup
cases, and exercises whose only goal is predicting a diagnostic.

### Priority 2: Major Standard-Library Areas

#### 5. Stream and File I/O

Progress: complete with
[20 validated exercises](collections/stream_and_file_io/collection_spec.md).

The text-processing collection uses string streams for parsing and formatting,
while the filesystem collection intentionally excludes file contents and stream
I/O. The dedicated stream and file-I/O collection now covers the practical
stream-state and file-content operations that fit Level A.

Strong exercise families include:

- Read one complete line with `std::getline`.
- Mix formatted extraction and line extraction without accidentally consuming an
  empty remainder.
- Read records or lines until EOF while distinguishing normal EOF from failure.
- Test, clear, and recover a stream state before continuing.
- Write a specified record through a supplied `std::ostream&`.
- Open file streams with the correct input, output, append, truncation, or binary
  mode and report open failure explicitly.
- Seek to a supplied input or output position, query positions, and patch output
  at a valid position.
- Read or write an exact bounded byte sequence and validate the transferred count.
- Copy through stream-buffer iterators when raw textual transfer is intended,
  including successful empty input and explicit output-failure detection.
- Borrow a C++20 string-stream buffer as a view or move it in or out where that
  avoids an unnecessary copy.
- Use `std::osyncstream` to emit one complete non-interleaved record, already
  covered by the concurrency collection rather than duplicated here.

Prefer deterministic tests using `std::istringstream`, `std::ostringstream`, or
caller-provided temporary paths. Do not depend on console interaction or
machine-specific files.

#### 6. Container-Specific Operations and Iterator Mechanics

Progress: complete with
[23 validated exercises](collections/container_operations_and_iterator_mechanics/collection_spec.md).

The core collection covers `std::vector`, associative containers, and container
adaptors well, and the ranges collection covers iterator/sentinel views. Several
high-value operations unique to other container and iterator categories are now
covered by this dedicated collection.

Strong exercise families include:

- Insert and remove values at both ends of a `std::deque`.
- Sort and merge linked sequences with the container-owned `std::list`
  operations that relink nodes instead of requiring random-access iterators.
- Transfer existing nodes with constant-time `std::list::splice`.
- Use `std::list::remove_if` and `std::list::unique`, including their C++20
  returned removal counts where useful.
- Use `std::forward_list::before_begin`, `insert_after`, and `erase_after`.
- Retrieve the complete value range associated with one `std::multimap` key.
- Merge compatible associative containers by transferring nodes.
- Reserve unordered-container capacity before known bulk insertion.
- Rehash or inspect load factor only when capacity behavior is the primary skill.
- Use `std::next`, `std::prev`, or `std::advance` with non-random-access
  iterators.
- Use `std::front_inserter` or general `std::inserter` when the destination's
  insertion position matters.
- Use reverse iterators directly when a view would not satisfy the supplied
  legacy interface, and convert a reverse position correctly for a forward
  iterator mutation interface.
- Consume the iterator and output fields of C++20 ranges algorithm result types.
- Use `std::ranges::iter_move` or `std::ranges::iter_swap` in a small generic
  operation where customization matters.

Do not mirror every ordinary vector operation across every container. Include a
container only when its interface or invalidation behavior teaches a meaningfully
different implementation pattern.

The completed collection deliberately stops short of separate `next` and `prev`
drills after covering non-random-access advancement, and does not add standalone
rehash or load-factor inspection exercises after teaching capacity reservation.
Those remaining candidates add mostly API symmetry rather than a distinct Level A
implementation skill.

#### 7. Practical Standard-Library Concepts

The templates-and-concepts collection teaches concept syntax and requires-
expression forms well, but practical selection from the standard concept
vocabulary is thin.

Strong exercise families include constraining a supplied interface with a
carefully chosen concept such as:

- `std::derived_from`.
- `std::constructible_from` or `std::assignable_from`.
- `std::equality_comparable` or `std::totally_ordered`.
- `std::movable`, `std::copyable`, or `std::regular`.
- `std::invocable`, `std::regular_invocable`, or `std::predicate`.
- `std::ranges::range`, `std::ranges::sized_range`, or
  `std::ranges::contiguous_range`.
- `std::input_iterator`, `std::forward_iterator`, or another iterator concept
  required by the supplied operation.

Teach selection of an appropriate existing concept for a real interface rather
than asking learners to memorize the complete concept hierarchy. Do not create
separate exercises for concepts whose practical contracts are indistinguishable
at Level A.

### Priority 3: Expand Already-Planned Collections

#### 8. Concurrency Scope Additions

Status: Done.

The completed concurrency collection has been audited against the expanded scope
below. Its current coverage includes:

- `std::future`, `std::promise`, and propagation of task exceptions.
- `std::async` with an explicit launch policy.
- `std::packaged_task` for connecting a callable to a future result.
- `std::shared_mutex` and `std::shared_lock` for read-mostly access.
- `std::call_once` for one-time initialization.
- `std::atomic_ref` for atomic access to supplied non-atomic storage.
- Atomic compare-and-exchange with correct expected-value handling.
- C++20 atomic waiting and notification without separate exercises for
  `notify_one` and `notify_all` when only wake cardinality differs.
- C++20 atomic `shared_ptr` release publication and acquire consumption, with
  ownership extension observable on the consuming side. Atomic `weak_ptr`
  remains excluded because it adds API symmetry without a distinct Level A
  ownership handoff.
- Relaxed ordering for an independent statistic that does not publish or consume
  unrelated state.
- Early release of `std::unique_lock` after copying a protected snapshot, so
  independent work stays outside the critical section.
- `std::osyncstream` for emitting one complete record without interleaving.

Tests must remain deterministic and must not rely on sleeps, timing races, or
probabilistic scheduling. Prefer supplied synchronization and explicit handoff
over attempts to reproduce data races.

No further concurrency additions are currently recommended at Level A. Shared
futures, non-blocking lock and semaphore variants, atomic `notify_one`, and
additional barrier operations remain plausible, but the available exercises are
primarily API symmetry or require supporting scenarios large enough to weaken
the one-minute format.

#### 9. Compile-Time Programming Scope Additions

Status: Done.

The completed compile-time programming collection has been audited against this
scope and covers:

- `std::is_constant_evaluated` for a function with distinct constant-evaluation
  and runtime implementation paths.
- Representative C++20 `constexpr` standard algorithms and utilities without
  repeating every runtime algorithm in a constant-evaluation wrapper.
- `constexpr` use of `std::vector` and `std::string` where the target standard
  library supports the required operations.
- Compile-time construction followed by a focused `static_assert`.
- The operational differences among `constexpr`, `consteval`, and `constinit`.
- C++20 constant evaluation involving temporary dynamic allocation whose storage
  is released before evaluation completes, only when supporting code keeps the
  learner task small.
- `constexpr` or immediate lambdas where the lambda form itself is meaningful.

Avoid recursive template metaprogramming, compiler-limit experiments, and tasks
that merely ask whether an expression happens to be accepted in constant
evaluation.

No further compile-time additions are currently recommended at Level A. The
collection deliberately retains only representative constant-evaluable
algorithms; additional algorithms, `constinit` storage variations, and immediate
function variations would repeat an existing primary skill. C++23 expansions
such as `if consteval`, constexpr smart pointers and bitsets, and constexpr
character conversion remain part of the separate C++23 delta roadmap.

### Priority 4: Focused Additions to Existing Areas

#### 10. Remaining Lambda Forms

Lambda coverage is already broad: ordinary predicates, value and initialized
captures, mutable state, move-only ownership, generic lambdas, explicit template
lists, pack captures, captureless closure construction, and lambda types in
unevaluated contexts are represented. A new large lambda collection is not
needed.

Only add exercises with distinct practical behavior, such as:

- Capture by reference when the callable must mutate a caller-owned object.
- Capture `*this` when a returned or deferred callable needs an object snapshot,
  contrasted with observing the original object through `this`.
- Convert a captureless lambda to a function pointer at a C-style callback
  boundary.
- Use a `constexpr` or immediate lambda in the compile-time collection.
- Use a generic forwarding lambda only if it does not duplicate the callable
  forwarding wrapper already present.

Explicit return types and `noexcept` lambda declarations are lower priority.
Avoid recursive-lambda algorithm exercises and lifetime traps involving returned
reference captures.

#### 11. Isolated High-Value C++20 Library Additions

Several practical C++20 facilities do not justify miscellaneous exercises with
no curricular home. Place each accepted exercise in the most natural existing or
future collection:

- `std::source_location` for caller-aware diagnostic context.
- `std::numbers` constants, including a typed constant where precision matters.
- `std::shift_left` and `std::shift_right` for in-place sequence shifting.
- `std::to_array` for converting a built-in array or literal-backed array into an
  owning `std::array`.
- `std::type_identity_t` for controlled deduction in the templates collection.
- `std::make_shared<T[]>` for shared array construction in the ownership
  collection.
- Actual heterogeneous unordered lookup after transparent hash and equality
  policies have been supplied.
- `std::atomic_ref`, two-sided atomic smart-pointer handoff, and synchronized
  output, now covered by the concurrency collection.
- `std::endian` only if embedded in a meaningful representation or protocol
  boundary rather than a one-line platform query.

Facilities such as `std::to_address`, overwrite-oriented smart-pointer factories,
and allocator-aware construction are lower-priority systems topics. Add them only
when a concrete, safe Level A objective remains after supporting machinery is
provided.

### Priority 5: Optional Specialized Coverage

The following areas can support valid exercises but should follow the priorities
above:

- `std::any`: construction, `has_value`, pointer-form `any_cast`, replacement,
  reset, and safe runtime inspection. This is the strongest optional area because
  it teaches open-ended runtime type erasure distinct from `std::variant`.
- `std::type_index` for using runtime types as ordered or unordered keys.
- `std::exception_ptr`, preferably as part of cross-thread error propagation.
- `std::uncaught_exceptions` only in a focused transactional RAII pattern.
- Polymorphic memory resources and `std::pmr` containers, including caller-
  supplied resources and monotonic allocation.
- A small amount of allocator-aware construction for learners targeting systems
  or library development.
- `std::complex` for a numerics-focused audience.

These topics are useful but less universal than the higher-priority language and
library gaps.

### Deliberate Non-Targets

Continue to omit or defer these areas unless the exercise format changes:

- Modules, because meaningful practice requires a multi-file build workflow.
- Coroutines at Level A; retain the longer Level B direction above.
- Implementing complete iterators, smart pointers, containers, allocators, or
  coroutine support types from scratch.
- Raw allocation, placement construction, explicit lifetime, and alignment
  puzzles as ordinary Level A material.
- `std::valarray`, locale facets, deprecated encoding conversion, C-style
  variadic functions, signals, non-local jumps, and termination-handler
  customization.
- Parallel execution-policy exercises whose toolchain linkage or observable
  behavior is not deterministic.
- Obscure C++20 delta items such as destroying delete, default-initialized
  bit-fields, nested inline namespaces, and class-type non-type template
  parameters unless a concrete high-value use case fits in Level A.
- Symmetric coverage of every remaining standard algorithm or container method.

### Suggested Review Order

When future sessions turn this audit into collection specifications, review the
areas in this order while continuing to let quality determine final size:

1. Class interfaces, special members, operators, and runtime polymorphism.
2. Type deduction, initialization, name resolution, and practical overload
   selection.
3. Stream and file I/O.
4. Concurrency with the expanded scope above.
5. Compile-time programming with the expanded scope above.
6. Container-specific operations and iterator mechanics.
7. Practical standard-library concepts.
8. Isolated high-value C++20 library additions.
9. Optional runtime type-erasure, diagnostics, PMR, and specialized numerics.

## C++23 Delta Collections

These topics should assume fluency with the completed up-to-C++20 collections and
test only a facility introduced by C++23 or a meaningfully new implementation
pattern that C++23 enables. Merely rewriting an earlier exercise with a newer
spelling is not enough.

Do not treat any exercise count as a quota. Determine collection size only after
drafting a manifest of distinct primary skills. Stop when the remaining
candidates are API symmetry, trivia, unsafe demonstrations, or repetitions of
up-to-C++20 work. The same Level A standard continues to apply: one clear
objective, normally about one minute of learner-written code, minimal supplied
machinery, and deterministic verification.

### Priority 1: Result Composition and Range-Centric Programming

#### 1. `std::expected`

`std::expected` is the strongest new C++23 vocabulary type and can support a
substantial collection, but its size should come from distinct state-handling and
composition skills rather than variations of the value and error types.

Strong exercise families include:

- Return an ordinary success value as an `std::expected<T, E>`.
- Return an error explicitly with `std::unexpected`.
- Construct an error in place with `std::unexpect` when the error has multiple
  constructor arguments.
- Return `std::expected<void, E>` for an operation that can succeed without a
  result value.
- Check `has_value` or use contextual conversion to `bool` before access.
- Read a value with `operator*` or `operator->` after the surrounding control flow
  establishes that it exists.
- Read the error on the failure path.
- Supply a fallback with `value_or` when eager fallback construction is suitable.
- Use checked `value()` only when throwing `std::bad_expected_access` is the
  specified boundary behavior.
- Replace an error state by constructing a value with `emplace`.
- Chain an expected-producing operation with `and_then`.
- Transform a successful value with `transform`.
- Recover or perform failure-side work with `or_else`.
- Convert an error representation with `transform_error`.
- Compose more than one operation while preserving the first failure.
- Convert a supplied exception-throwing or sentinel-returning interface into an
  explicit expected result.
- Compare expected results only where equality is part of a real contract.

Keep parsing, validation, lookup, and conversion logic supplied or deliberately
small. The exercise objective is result modelling or composition, not discovering
the underlying algorithm. Do not manufacture separate exercises solely for
const, non-const, lvalue, and rvalue overloads of the same monadic operation.

#### 2. Monadic `std::optional`

The C++23 delta is the addition of monadic operations, not ordinary optional
construction and access, which are already covered up to C++20.

Strong exercise families include:

- Chain an optional-producing function with `and_then`.
- Transform a contained value without introducing a nested optional.
- Supply a lazily computed alternative with `or_else`.
- Compose two or three optional operations without nested conditionals.
- Preserve move-only contained state through a composition when the value
  category is part of the supplied interface.
- Contrast `transform` with `and_then` in tasks where one callback returns a
  value and the other returns an optional.

A compact collection is preferable. Repeating the three operations with
different scalar types or callback spellings does not create new skills.

#### 3. Ranges-Aware Container and String Construction and Mutation

This is a major C++23 delta distinct from `std::ranges::to`. It should have an
explicit curricular owner rather than being hidden inside miscellaneous ranges
exercises.

Strong exercise families include:

- Construct a container from an input range with the `std::from_range` tag.
- Construct from a transformed or filtered view without first creating an
  intermediate container.
- Replace a sequence container's contents with `assign_range`.
- Insert a range at a specified position with `insert_range`.
- Insert after a predecessor in `std::forward_list` with `insert_range_after`.
- Append a range to a sequence with `append_range`.
- Prepend a range to a `std::deque` with `prepend_range`.
- Insert a range of values into an associative container.
- Use a string's `assign_range`, `append_range`, `insert_range`, or
  `replace_with_range` when the source is naturally expressed as a range.
- Preserve the source order and respect iterator invalidation when surrounding
  code retains positions in the destination.

Choose exercises by distinct construction or mutation semantics, not by taking
the Cartesian product of every method and every container. In particular,
ordinary associative lookup and ordinary iterator-pair insertion are not C++23
skills.

#### 4. Ranges Materialization and Folds

Strong exercise families include:

- Materialize a view into an explicitly named destination type with
  `std::ranges::to<C>`.
- Let `std::ranges::to` deduce a container specialization from a container
  template where that improves the interface.
- Use the pipe form of `std::ranges::to` at the end of a view pipeline.
- Materialize nested ranges only when recursive conversion is the actual skill.
- Fold left with an explicit initial value.
- Fold right where operand order is observable.
- Use `fold_left_first` or `fold_right_last` when the first or last range element
  supplies the initial value.
- Handle the optional result of a fold without an explicit initial value.
- Retain the final iterator with `fold_left_with_iter` or
  `fold_left_first_with_iter` when processing may stop at a supplied sentinel.
- Fold values whose accumulator type differs from the range value type.

Avoid duplicating `std::accumulate` exercises unless operand order, range
constraints, lack of an explicit initial value, or the returned iterator makes
the C++23 operation meaningfully different.

#### 5. C++23 Range Algorithms

Strong exercise families include:

- Test membership with `std::ranges::contains`, including one useful projection.
- Test for a contiguous subsequence with `contains_subrange`.
- Test a prefix or suffix of an arbitrary range with `starts_with` or
  `ends_with`.
- Find the final matching value with `find_last`.
- Find the final element satisfying or rejecting a predicate with `find_last_if`
  or `find_last_if_not`.
- Fill a supplied range with increasing values using `ranges::iota`.
- Shift elements left or right in place and use the returned subrange correctly.

Do not create separate exercises for iterator and range overloads unless the
bounded subrange or returned result changes how the learner must implement the
operation. Prefer projections and returned iterator/subrange consumption over
cosmetic predicate variations.

#### 6. C++23 Range Views

The number of new adaptors can support a large collection, but each exercise
must expose the adaptor's distinctive behavior:

- `zip` for lockstep traversal of two or more ranges, stopping at the shortest.
- `zip_transform` when transforming corresponding elements is the complete
  operation.
- `enumerate` for index-and-value traversal without maintaining an external
  counter.
- `adjacent<N>` for overlapping fixed-size groups.
- `adjacent_transform` for direct neighboring-value computation.
- `chunk` for non-overlapping fixed-size groups, including a shorter final group.
- `chunk_by` for maximal adjacent groups sharing a supplied relation.
- `slide` for overlapping windows of runtime width.
- `stride` for selecting every nth element.
- `join_with` for flattening nested ranges with an intervening separator range or
  value.
- `cartesian_product` for direct product traversal when output size is deliberately
  small.
- Finite and unbounded forms of `repeat`, with an explicit bound for consumption
  of an unbounded view.
- `as_const` for read-only traversal through a shallow-const range or view.
- `as_rvalue` when consuming elements from a range as rvalues is intentional.
- One reusable pipeable adaptor using `std::ranges::range_adaptor_closure`, with
  the adaptor's core type and invariant supplied so the learner task stays Level
  A.

Do not turn adaptor use into an algorithm-discovery problem. Avoid multiple
exercises that differ only in the element type or in whether a pipeline is
written with `|` or nested calls.

#### 7. Constant Iterators, Constant Ranges, and Range Interoperability

C++23 completes important const-iteration machinery beyond `views::as_const`.
This area deserves a small focused family:

- Wrap a mutable iterator with `std::make_const_iterator` before exposing it.
- Pair a const iterator with `std::make_const_sentinel` for a supplied
  iterator-sentinel range.
- Use `std::const_iterator` or `std::basic_const_iterator` in a small read-only
  legacy iterator interface.
- Constrain an operation with `std::ranges::constant_range` when read-only
  dereference is a real requirement.
- Obtain a range's C++23 constant iterator or constant reference type with
  `std::ranges::const_iterator_t` or `std::ranges::range_const_reference_t` in a
  supplied generic declaration.
- Use a move-only callable in a range adaptor where C++23's relaxed adaptor
  storage is the enabling change.
- Pass compatible C++20 ranges iterators to a legacy non-ranges algorithm where
  C++23 repairs the interoperability problem.

The generic type machinery should be supplied when it would dominate the task.
Do not ask learners to implement an iterator adaptor from scratch.

### Priority 2: Output, Data Layout, Containers, and Coroutines

#### 8. Formatted Output and Range Formatting

Strong exercise families include:

- Print formatted values with `std::print`.
- Print a complete record followed by a newline with `std::println`.
- Print to a supplied `std::FILE*` where that boundary is already established.
- Format or print a standard sequence or associative container.
- Format tuple-like values.
- Use escaped/debug presentation for a character or string whose delimiters and
  control characters must be visible.
- Apply supported range-format options when they materially change the output.
- Format a thread identifier or stack trace only in the collection that owns the
  underlying facility.
- Use `std::range_formatter`, `std::range_format`, or `std::format_kind` only with
  a supplied custom range-like type and a small, explicit formatting goal.

C++23 `std::print` uses compile-time-checked format-string interfaces.
`std::runtime_format` is not a C++23 facility; runtime formatting through earlier
`vformat` machinery is not itself a C++23-delta exercise. Tests should capture a
stream or file and compare deterministic bytes rather than depend on terminal
behavior.

#### 9. `std::mdspan`

Strong exercise families include:

- Construct a two-dimensional non-owning view over contiguous storage.
- Access or update an element with multidimensional indexing.
- Construct a three-dimensional view when the indexing pattern remains the only
  task.
- Combine static and dynamic extents.
- Query rank, extents, and the size of a particular dimension.
- Use `layout_right` and `layout_left` where the supplied storage order makes the
  difference observable.
- Use `layout_stride` with an already specified padded or strided representation.
- Inspect a mapping's stride or required span size.
- Pass an `mdspan` to a function without copying the underlying data.
- Use a custom accessor only when it is supplied and the learner merely selects
  or applies it.

Do not ask learners to implement a layout mapping or accessor policy. Avoid
matrix algorithms whose difficulty comes from the algorithm rather than the
non-owning multidimensional interface.

#### 10. Flat Associative Containers

Exercises should concentrate on behavior that distinguishes flat containers
from `map`, `multimap`, `set`, and `multiset`:

- Construct a `flat_map`, `flat_multimap`, `flat_set`, or `flat_multiset` where
  sorted contiguous storage is an appropriate supplied requirement.
- Construct from already sorted unique or equivalent data with the corresponding
  tag when the precondition is explicit.
- Insert a range while preserving the container's ordering and uniqueness
  contract.
- Retrieve the underlying key and mapped sequences with `keys()` and `values()`.
- Transfer out the underlying containers with `extract`.
- Replace the underlying containers with `replace` after the surrounding code
  establishes their invariants.
- Account for iterator invalidation after insertion or erasure.
- Select a flat container over a node-based associative container when iteration
  locality and infrequent mutation are stated requirements.

Ordinary `find`, `contains`, bounds queries, `operator[]`, `try_emplace`, and
`insert_or_assign` should not be repeated merely because the owning type is flat.
Use them only when coupled to a distinctive flat-container operation.

#### 11. `std::generator`

Generator exercises can fit Level A when the return type and surrounding
coroutine structure are small or supplied:

- Consume a generator as an input range.
- Yield a short sequence of calculated values with `co_yield`.
- Stop generation at a supplied condition to demonstrate laziness.
- Yield references safely from storage whose lifetime is guaranteed by the
  caller.
- Yield move-only values where ownership transfer is explicit.
- Flatten a supplied range or nested generator with
  `std::ranges::elements_of`.
- Compose a generator with ordinary range adaptors.
- Make the lifetime relationship between generator state and captured or
  referenced data explicit.

Do not ask learners to implement a promise type, coroutine frame, or generator
class. Avoid exercises whose correctness depends on subtle temporary lifetimes
that the task does not make explicit.

### Priority 3: Callable, Text, I/O, and Compile-Time Facilities

#### 12. Move-Only Callables and Callable Utilities

Strong exercise families include:

- Store a lambda with a move-only capture in `std::move_only_function`.
- Accept or transfer ownership of a move-only callback.
- Invoke and replace a stored move-only callback.
- Use a cv-, ref-, or `noexcept`-qualified `move_only_function` signature when the
  supplied callable contract requires it.
- Bind trailing arguments with `std::bind_back`.
- Use `std::invoke_r` to invoke a callable with an explicitly requested result
  type.
- Apply cv/ref qualification modeled on another expression with
  `std::forward_like`.
- Use `forward_like` inside a supplied explicit-object accessor to preserve the
  containing object's constness and value category.

Do not repeat existing `std::function`, `std::bind_front`, `std::invoke`, or
perfect-forwarding exercises unless the new C++23 facility changes ownership,
argument position, or result typing.

#### 13. C++23 String and Stream Facilities

Strong exercise families include:

- Test substring or character presence with `std::string::contains`.
- Test presence in a non-owning `std::string_view`.
- Populate a string's writable storage with `resize_and_overwrite` and return the
  actual produced length.
- Read formatted values from an existing character buffer with
  `std::ispanstream`.
- Write formatted data into caller-owned storage with `std::ospanstream` and
  retrieve the written span.
- Read and write through `std::spanstream` when both directions are required.
- Construct an explicit `std::string_view` from a suitable contiguous sized
  range whose lifetime is already guaranteed.
- Use the rvalue-qualified `std::string::substr` when consuming a temporary or
  movable string makes the ownership intent clear.
- Open an output file exclusively with `std::ios::noreplace` and report an
  already-existing target without overwriting it.

Use caller-provided buffers and temporary paths so tests remain deterministic.
Do not turn buffer production into a parsing or encoding problem.

#### 14. C++23 Compile-Time Library Expansion

This family complements the core-language constant-evaluation changes below.
Every exercise should perform useful compile-time work with a facility whose
`constexpr` support is new in C++23:

- Build or transform a `constexpr std::bitset` and verify the result with
  `static_assert`.
- Use a temporary `std::unique_ptr` during constant evaluation while ensuring
  its allocation is released before evaluation completes.
- Convert an integer to characters during constant evaluation with
  `std::to_chars`.
- Parse an integer during constant evaluation with `std::from_chars` and inspect
  the returned pointer and error code.
- Use one of the newly constant-evaluable `<cmath>` or `<cstdlib>` operations
  where the operation has a clear numerical purpose.
- Compare supplied `std::type_info` objects during constant evaluation only if a
  concise portable exercise can make the result meaningful.

Do not copy runtime exercises and add `constexpr` mechanically. Exclude
compiler-limit experiments and constant-evaluation tasks whose only outcome is
that the source compiles.

#### 15. Focused Container, Type-Trait, and Utility Additions

These facilities are useful but too small or too varied to justify arbitrary
standalone collections. Place each accepted exercise with its natural owner:

- Erase from an ordered associative container using a heterogeneous key and a
  supplied transparent comparator.
- Erase from an unordered associative container using a heterogeneous key and
  supplied transparent hash and equality policies.
- Construct `std::queue` or `std::stack` from an iterator pair when the source is
  not already the desired underlying container.
- Convert an enumeration value with `std::to_underlying`.
- Reverse an integral object's byte order with `std::byteswap` at a specified
  representation boundary.
- Detect a scoped enumeration with `std::is_scoped_enum` in a small generic
  interface.
- Prevent a dangling reference with `std::reference_constructs_from_temporary`
  or `std::reference_converts_from_temporary` in a supplied constraint or
  assertion.
- Use C++23 tuple-like construction, assignment, comparison, `common_type`, or
  `common_reference` interoperability among `tuple`, `pair`, `array`, and
  `ranges::subrange` when the conversion has an observable purpose.

Do not create one exercise per container for heterogeneous erasure or one
exercise per enum for the same utility. Low-level traits such as
`std::is_implicit_lifetime` belong with the specialized lifetime material below.

### Priority 4: C++23 Core-Language Delta

#### 16. Explicit Object Parameters

Strong exercise families include:

- Share one implementation between const and non-const member access.
- Preserve the explicit object's value category in a forwarding accessor.
- Combine an explicit object parameter with `std::forward_like` to return the
  corresponding member correctly.
- Write a recursive lambda by passing the closure object explicitly.
- Express a mixin operation that returns the concrete derived object.
- Replace a supplied duplicated cv/ref-qualified overload set with one explicit-
  object member function.

Keep class and mixin scaffolding supplied. Do not turn the exercise into template
architecture or CRTP design.

#### 17. Constant-Evaluation Language Improvements

Strong exercise families include:

- Select a compile-time implementation path with `if consteval`.
- Use `if !consteval` where the runtime path is the exceptional branch.
- Put a static constant lookup table in a `constexpr` function.
- Allow a non-literal local variable only on a runtime branch of a `constexpr`
  function.
- Write a `constexpr` function whose parameter or result type need not itself be
  a literal type, while constant-evaluable calls remain meaningful.
- Separate immediate validation from runtime behavior without duplicating the
  common operation.

Do not reward `goto` or labels merely because C++23 permits them in additional
`constexpr` contexts. The relaxed rule should enable clearer useful code.

#### 18. New Call and Subscript Forms

Strong exercise families include:

- Implement or use a multidimensional `operator[]` for a supplied small view or
  fixed-layout wrapper.
- Declare a stateless function object's `operator()` as static.
- Declare a supplied indexing policy's `operator[]` as static.
- Use a captureless static lambda where its non-member-like call semantics are
  relevant.

These forms are a small family. Do not create variations by changing only the
number of indices, arithmetic formula, or wrapped scalar type.

#### 19. Explicit Decay Copy and Simpler Implicit Move

Strong exercise families include:

- Use `auto(expression)` to create an intentional decay copy in generic code.
- Use `auto{expression}` where list initialization is the required decay-copy
  form.
- Return a local move-eligible object without an explicit `std::move`.
- Return or pass through a move-eligible function parameter under C++23's simpler
  implicit-move rules.
- Make the resulting ownership transfer or independence from a referenced source
  observable.

Avoid exercises that ask only for `return value;` without surrounding types that
make the C++23 rule the unmistakable objective.

#### 20. Range-For Lifetime Extension

C++23 extends the lifetimes of temporary objects in a range initializer in
additional cases. This is a small but important lifetime-safety delta.

Strong exercise families include:

- Iterate directly over a range subobject obtained from a temporary owner where
  C++23 now keeps the relevant temporary alive.
- Compose a temporary range-producing expression in a range-for initializer when
  the returned range safely refers into that temporary.
- Retain an init-statement owner when an intermediate function parameter would
  still produce a dangling reference even in C++23.

Teach a correct form and make ownership visible. Do not ask learners to execute
or diagnose a pre-C++23 dangling loop, and do not imply that C++23 repairs
functions that return references to destroyed by-value parameters.

#### 21. Focused Syntax, Deduction, and Literal Improvements

Only a small number of these features produce worthwhile implementation
exercises:

- Use `z` or `uz` integer literal suffixes where matching a container's signed or
  unsigned size type avoids a conversion.
- Use `#elifdef` or `#elifndef` in a supplied compact configuration branch.
- Apply class template argument deduction through inherited constructors in a
  supplied small hierarchy.
- Use a named universal character escape for a recognizable Unicode character.
- Use a delimited hexadecimal, octal, or Unicode escape where the delimiter
  removes ambiguity.
- Apply a lambda attribute such as `[[nodiscard]]` only when it creates a real
  callable contract and the toolchain can verify it deterministically.

Omitting empty lambda parentheses before specifiers is valid C++23 syntax but is
too small to own an exercise. Alias declarations in init-statements, narrowing
contextual conversions to `bool`, and extended source-character rules should be
included only when a concrete task remains after all supporting code is supplied.

### Priority 5: Specialized or Environment-Dependent Coverage

#### 22. C Interoperability and Explicit Lifetime Utilities

Potential specialized exercises include:

- Adapt a `std::unique_ptr` to a supplied C output-parameter function with
  `std::out_ptr`.
- Replace an existing smart-pointer-managed resource through a supplied C API
  with `std::inout_ptr`.
- Preserve a custom deleter or pointer type while using those adaptors.
- Request at least a specified allocation size with `std::allocate_at_least` in
  allocator-focused code.
- Begin the lifetime of an implicit-lifetime object with
  `std::start_lifetime_as` only at a real byte-storage or interoperability
  boundary.
- Use `std::is_implicit_lifetime` to constrain such a supplied lifetime utility.
- Use `<stdatomic.h>` only when direct C-header interoperability is the actual
  objective.

`out_ptr` and `inout_ptr` can fit Level A because the C function and ownership
wrapper can be supplied. `start_lifetime_as`, allocator feedback, and related
traits are systems-level material; do not turn them into raw-storage puzzles or
ordinary curriculum requirements.

#### 23. Diagnostics

At most a small observational family is warranted:

- Capture the current `std::stacktrace` at a specified diagnostic boundary.
- Store or pass a stack trace without depending on exact symbol names.
- Format or print a captured stack trace when formatting support is available.

Tests should verify stable structural properties or supplied formatting hooks,
not platform-specific frame counts, addresses, paths, or symbol quality.

#### 24. Modules and Extended Floating-Point Types

- Standard-library modules `std` and `std.compat` require a multi-file/module-aware
  build workflow and should remain deferred until such a practice format exists.
- `std::float16_t`, `std::float32_t`, `std::float64_t`, `std::float128_t`, and
  `std::bfloat16_t` are optional extended floating-point types. Exercises should
  be generated only for types the target environment provides, and should teach
  a meaningful precision or interchange boundary rather than type-name trivia.

### Deliberate C++23 Non-Targets

Continue to omit these even when the implementation supports them, unless a
future exercise format creates a concrete and safely testable objective:

- `[[assume]]` and `std::unreachable` as ordinary exercises. Violating their
  contracts is undefined behavior, while satisfying them normally has no
  portable observable result.
- `#warning`, because emitting a diagnostic is not a successful implementation
  outcome for the current compiler-driven workflow.
- Labels at the end of compound statements, whitespace trimming before line
  splicing, mandated member declaration order, and standards wording changes
  that require no implementation decision.
- Removed garbage-collection hooks, deprecated `aligned_storage` and
  `aligned_union`, removed mixed wide-literal concatenation, and other migration
  trivia unless a separate modernization collection is requested.
- Full coroutine promise types, custom generator implementations, layout mapping
  implementations, iterator implementations, or allocator implementations.
- Runtime-format-string exercises labeled as C++23 work; the C++23 delta is
  formatted output and range/tuple formatting, not `std::runtime_format`.
- Symmetric repetition of the same new method across every compatible container,
  every cv/ref overload of one operation, or every flat-container equivalent of
  an existing node-container exercise.

### Portability and Feature Boundaries

Define each collection against the C++23 standard rather than a vendor extension.
Before generating a batch, record the relevant language and library feature-test
macros in its collection specification and verify that the chosen target
environment implements the standard facility. If a facility is unavailable,
defer that exercise family; do not emulate it with a third-party or vendor API
while continuing to label the result as a C++23-delta exercise.

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

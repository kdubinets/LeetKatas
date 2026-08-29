Generate approximately 30 Level A C++20 implementation-fluency exercises.

The exercises are not intended to test algorithm discovery or problem-solving. They should train fast, idiomatic use of C++20 language features, standard containers, iterators, algorithms, ranges, lambdas, utilities, and common implementation patterns.

A person who already understands the required operation and types reasonably quickly should normally complete each exercise in one minute or less.

## Output structure

For every exercise, create exactly two files with the same unique basename:

* `<basename>.cpp`
* `<basename>.md`

Use descriptive lowercase snake_case basenames, such as:

* `check_map_membership.cpp`
* `check_map_membership.md`

Do not create additional files unless explicitly requested.

## C++ file requirements

Each `.cpp` file must contain exactly the code presented to the learner.

It must:

* Target C++20.
* Be self-contained apart from the unfinished practice section.
* Include all necessary standard-library headers.
* Contain minimal supporting code.
* Avoid unnecessary domain models, realistic scenarios, frameworks, input parsing, logging, and boilerplate.
* Contain exactly one unfinished practice section.
* Mark that section with exactly this form:

`// Finish: <brief description of what needs to be done>`

The description after `Finish:` must explain the required result without revealing the intended API, standard algorithm, container method, language feature, or implementation technique.

Good:

`// Finish: return whether the key is present`

Bad:

`// Finish: use contains() to check whether the key is present`

Good:

`// Finish: sort the records by descending score and then ascending id`

Bad:

`// Finish: call std::ranges::sort with a lambda`

The marker may replace:

* One expression.
* One statement.
* Several related statements.
* A small function body.

Keep the unfinished portion small enough to complete in about one minute or less.

The surrounding code should make the required types, inputs, output, mutation rules, and relevant constraints clear.

The `.cpp` file must be self-sufficient. The learner sees only the `.cpp` file while solving; the `.md` file is revealed afterwards. Every behavioral requirement the learner is expected to satisfy must therefore be stated in, or directly inferable from, the signature, the types, and the `Finish:` marker text. Requirements that commonly leak into the metadata alone include empty-input and other edge-case behavior, whether the input may be modified, whether copying is permitted, tie-breaking rules, and required result types for absent values. State such a requirement in the marker text, which constrains the result without naming the API or technique used to achieve it.

Good:

`// Finish: move the first value to the end while preserving the order of all other values, doing nothing when empty`

Bad:

`// Finish: move the first value to the end`

with the empty-input rule appearing only in the metadata description.

Prefer small functions such as:

```
bool solve(const std::unordered_map<int, int>& values, int key) {
    // Finish: return whether the key is present
}
```

Do not add explanatory comments other than the required `// Finish:` comment unless a comment is essential for expressing a constraint that cannot be represented clearly in code.

Do not include the solution in the `.cpp` file.

Do not include multiple independent tasks in one exercise.

## Metadata file requirements

Each `.md` file must contain exactly these sections:

# Name

A short human-readable name that helps the learner distinguish the exercise.

# Description

A concise description of:

* What operation the learner must implement.
* The important input and output types.
* Relevant behavioral constraints, such as whether the input may be modified.
* What implementation skill the exercise covers.

The description restates and records requirements; it must never introduce one. Every constraint it names must already be visible in the `.cpp` file.

Close the description with one curriculum annotation of the form `This exercise covers <skill>.` naming the skill the exercise trains. This annotation is bookkeeping for the manifest and for duplicate detection. It records why the exercise exists and never states a requirement, so it may name a technique, facility, or complexity class that the marker text deliberately withholds from the learner. Keep this exact sentence form: the review harness relies on it to distinguish the annotation from the specification.

This description will also be used by future LLM runs to detect exercises that have already been generated. Make it specific enough to distinguish the exercise from similar exercises.

Do not mention the exact solution API unless naming it is necessary to identify the skill being tracked.

# Solution

A C++ code block containing exactly the code that must replace the complete `// Finish: ...` comment line.

Do not repeat the surrounding function or file.

For example:

````
# Solution

```cpp
return values.contains(key);
```
````

For a multi-statement answer, include only those statements:

````
# Solution

```cpp
auto it = values.find(key);
return it == values.end() ? 0 : it->second;
```
````

The solution must compile correctly when substituted for the comment.

## Exercise granularity

Each exercise must test one atomic implementation skill or one tightly coupled group of statements.

Appropriate examples include:

* Check whether a key exists in a map.
* Read a mapped value without inserting a missing key.
* Increment a frequency count.
* Insert only when a key is absent.
* Remove a map entry safely while iterating.
* Sort values in ascending or descending order.
* Sort records by one or two fields.
* Find a lower or upper bound.
* Convert an iterator position to an index.
* Count elements matching a predicate.
* Check whether any, all, or no elements match.
* Find an element with a predicate.
* Transform one range into another.
* Accumulate values.
* Remove matching elements from a vector.
* Remove adjacent duplicates from a sorted vector.
* Reverse or rotate a range.
* Partition a range.
* Create and use a min-heap.
* Push and retrieve structured heap entries.
* Use structured bindings.
* Use `std::optional`.
* Use `std::pair` or `std::tuple`.
* Iterate with indices safely.
* Iterate over map keys and values.
* Construct a set from a range.
* Append one vector to another.
* Extract a substring or split a simple string.
* Compare strings or records using a custom rule.
* Clamp a value or compute a minimum or maximum.
* Exchange or move values.
* Initialize a two-dimensional vector.
* Use a lambda with a capture.
* Use a projection or a range-based standard algorithm where appropriate.

Inappropriate exercises include:

* Discovering a sliding-window algorithm.
* Implementing graph traversal.
* Designing dynamic programming state.
* Solving a complete LeetCode problem.
* Writing a long parser.
* Implementing a data structure from scratch.
* Tasks requiring substantial edge-case reasoning.
* Tasks requiring more than roughly ten lines of learner-written code.
* Trivia about obscure language behavior.

## Content selection

Generate a varied set of approximately 30 exercises.

Cover a balanced selection of:

* `std::vector`
* `std::string`
* `std::array`
* `std::unordered_map`
* `std::map`
* `std::unordered_set`
* `std::set`
* `std::queue`
* `std::stack`
* `std::priority_queue`
* Iterators
* Standard algorithms
* C++20 ranges
* Lambdas
* Structured bindings
* `std::optional`
* Pairs and tuples

Do not force every listed topic into the set. Prefer common interview implementation skills over broad library coverage.

Avoid near-duplicate exercises. Variations are acceptable only when they train meaningfully different behavior, such as:

* Mutating versus non-mutating sorting.
* Membership checking versus retrieving a value.
* Ascending versus multi-field ordering.
* Erasing one element versus erasing while iterating.
* Returning an iterator versus returning an index.
* Operating on values versus operating on records.

Prefer clear, conventional interview code over clever, compressed, obscure, or highly specialized C++.

Use C++20 features when they improve clarity, but do not use ranges or advanced syntax merely to make the solution look modern.

## Correctness requirements

Before finalizing each pair of files, verify that:

* The `.cpp` file becomes valid C++20 after replacing the comment with the metadata solution.
* Required headers are present.
* The solution matches all constness and mutation constraints.
* There are no accidental copies of large containers when references are appropriate.
* Signed and unsigned conversions are handled sensibly.
* Comparators define valid strict weak ordering.
* Map access does not accidentally insert keys unless insertion is intended.
* Iterator invalidation is handled correctly.
* The solution is idiomatic and concise without being cryptic.
* The exercise has exactly one reasonable primary implementation objective.
* The learner-written portion should normally take no more than one minute.
* Every behavioral requirement in the metadata description is also stated in, or inferable from, the `.cpp` file. A requirement the learner could satisfy only by reading the metadata belongs in the marker text instead.

## Final review

After generating all files, inspect the complete set for duplication.

Replace exercises that test essentially the same operation with different variable names.

Ensure the final collection emphasizes reusable implementation fluency rather than algorithmic problem-solving.

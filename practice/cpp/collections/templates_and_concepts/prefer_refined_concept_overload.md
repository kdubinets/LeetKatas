# Name

Prefer a Refined Concept Overload

# Description

Overload `category` for `WholeNumber` values and return `"whole"`. Its constraint must preserve the declared refinement so overload ordering prefers it over the existing `Number` overload for integral arguments.

# Solution

```cpp
template <WholeNumber T>
constexpr std::string_view category(T) {
    return "whole";
}
```

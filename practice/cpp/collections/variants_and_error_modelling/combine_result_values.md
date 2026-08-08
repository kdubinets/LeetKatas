# Name

Combine Two Explicit Results

# Description

Combine two integer-or-error results into a pair when both succeeded. If either failed, propagate the first error in left-to-right order without attempting to manufacture a value.

# Solution

```cpp
if (const auto* error = std::get_if<Error>(&left)) {
    return *error;
}
if (const auto* error = std::get_if<Error>(&right)) {
    return *error;
}
return std::pair{std::get<int>(left), std::get<int>(right)};
```

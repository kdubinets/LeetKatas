# Name

Copy Positive Values

# Description

Build a new integer vector containing only the positive values from a const input vector, preserving their relative order and leaving the input unchanged. This exercise covers predicate-controlled copying through an output iterator.

# Solution

```cpp
std::ranges::copy_if(values, std::back_inserter(result),
                     [](int value) { return value > 0; });
```

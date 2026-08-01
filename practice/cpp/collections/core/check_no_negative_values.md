# Name

Check No Negative Values

# Description

Return whether a const integer vector contains no values below zero; an empty vector satisfies the condition. This exercise covers testing that no range element matches a predicate.

# Solution

```cpp
return std::ranges::none_of(values, [](int value) { return value < 0; });
```

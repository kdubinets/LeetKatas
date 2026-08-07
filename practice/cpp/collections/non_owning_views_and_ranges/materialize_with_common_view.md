# Name

Materialize with a Common View

# Description

Materialize the supplied finite lazy integer view into a vector using an iterator-pair constructor. All generated integers are representable. Its iterator and sentinel initially have different types, so first adapt it to use one common type. This exercise covers bridging iterator/sentinel ranges to legacy iterator-pair interfaces.

# Solution

```cpp
auto common_values = values | std::views::common;
return {common_values.begin(), common_values.end()};
```

# Name

Default Three-Way Comparison

# Description

Give a two-field value type generated equality and lexicographic ordering in declaration order. Use C++20's concise memberwise comparison definition.

# Solution

```cpp
auto operator<=>(const PathPart&) const = default;
```

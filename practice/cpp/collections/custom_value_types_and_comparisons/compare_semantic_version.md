# Name

Compare a Semantic Version

# Description

Implement strong lexicographic ordering of three integer version components in major, minor, patch order. Compose existing tuple comparison rather than writing branching logic.

# Solution

```cpp
return std::tie(left.major, left.minor, left.patch)
    <=> std::tie(right.major, right.minor, right.patch);
```

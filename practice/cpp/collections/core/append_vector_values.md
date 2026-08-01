# Name

Append Vector Values

# Description

Append all integers from a const source vector to a mutable destination vector, preserving both vectors' existing order and leaving the source unchanged. This exercise covers inserting an iterator range at a sequence endpoint.

# Solution

```cpp
destination.insert(destination.end(), source.begin(), source.end());
```

# Name

Push Structured Priority Entry

# Description

Add a `(priority, id)` integer entry to a mutable max-priority `std::priority_queue<std::pair<int, int>>`. The queue's existing lexicographic pair ordering remains in effect. This exercise covers in-place construction of structured heap entries.

# Solution

```cpp
tasks.emplace(priority, id);
```

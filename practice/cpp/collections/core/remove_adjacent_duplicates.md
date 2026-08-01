# Name

Remove Adjacent Duplicates

# Description

Given a mutable sorted `std::vector<int>`, remove repeated adjacent occurrences so that exactly one copy of each distinct value remains. This exercise covers combining duplicate compaction with physical vector erasure.

# Solution

```cpp
auto duplicates = std::ranges::unique(sorted_values);
sorted_values.erase(duplicates.begin(), duplicates.end());
```

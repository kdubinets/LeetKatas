# Name

Materialize a Counted Range

# Description

Given a const vector and a valid segment described by `start` and `count`, copy that segment into a new vector. Represent the source segment through its first iterator and element count rather than computing an end iterator. This exercise covers a counted view.

# Solution

```cpp
using difference_type = std::vector<int>::difference_type;
auto counted = std::views::counted(
    values.begin() + static_cast<difference_type>(start),
    static_cast<difference_type>(count));
std::ranges::copy(counted, std::back_inserter(result));
```

# Name

Flatten Nested Ranges

# Description

Copy all integers from a const vector of vectors into one vector, preserving both row order and order within each row. Traverse the nested input as one lazy flattened range. This exercise covers `std::views::join` followed by explicit C++20 materialization.

# Solution

```cpp
auto flattened = rows | std::views::join;
std::ranges::copy(flattened, std::back_inserter(result));
```

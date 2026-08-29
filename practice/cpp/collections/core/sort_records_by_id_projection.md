# Name

Sort Records by ID

# Description

Sort a mutable vector of `Record` objects in place by ascending integer ID. Scores do not affect ordering. This exercise covers member projection in a C++20 range algorithm.

# Solution

```cpp
std::ranges::sort(records, {}, &Record::id);
```

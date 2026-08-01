# Name

Stable Sort Records by Group

# Description

Sort a mutable vector of records by ascending integer group while preserving the original relative order of records whose groups are equal. IDs do not otherwise affect ordering. This exercise covers stable sorting through a member projection.

# Solution

```cpp
std::ranges::stable_sort(records, {}, &Record::group);
```

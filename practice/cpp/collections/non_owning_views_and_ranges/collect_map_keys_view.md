# Name

Collect Map Keys Through a View

# Description

Copy only the string keys of a const ordered map into a vector in map iteration order. Traverse the pair-like entries through a lazy key-field view. This exercise covers `std::views::keys` and C++20 materialization.

# Solution

```cpp
auto keys = values | std::views::keys;
std::ranges::copy(keys, std::back_inserter(result));
```

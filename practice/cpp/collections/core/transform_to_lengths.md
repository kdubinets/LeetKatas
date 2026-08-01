# Name

Transform Strings to Lengths

# Description

Build and return a `std::vector<std::size_t>` containing the length of every string from a const input vector in the same order. The pre-reserved output should be populated without modifying the input. This exercise covers range transformation into an output iterator.

# Solution

```cpp
std::ranges::transform(values, std::back_inserter(lengths),
                       [](const std::string& value) { return value.size(); });
```

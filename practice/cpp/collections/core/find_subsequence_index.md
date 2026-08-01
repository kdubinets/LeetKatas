# Name

Find Subsequence Index

# Description

Find the first contiguous occurrence of a const integer pattern vector inside another const integer vector and return its starting index. Return zero for an empty pattern and an empty optional when a nonempty pattern is absent. This exercise covers searching for one range inside another.

# Solution

```cpp
if (pattern.empty()) {
    return std::size_t{0};
}
auto match = std::ranges::search(values, pattern);
return match.begin() == values.end()
           ? std::nullopt
           : std::optional<std::size_t>{
                 static_cast<std::size_t>(match.begin() - values.begin())};
```

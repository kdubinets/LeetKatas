# Name

First Vector Mismatch Index

# Description

Return the first `std::size_t` position where two const integer vectors have different values. If one is an exact prefix of the other, return the shorter length; if they are equal, return an empty optional. This exercise covers paired-range mismatch detection and iterator positioning.

# Solution

```cpp
auto [left_it, right_it] = std::ranges::mismatch(left, right);
if (left_it == left.end() && right_it == right.end()) {
    return std::nullopt;
}
return static_cast<std::size_t>(left_it - left.begin());
```

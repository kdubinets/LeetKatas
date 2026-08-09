# Name

Build a Constexpr Lookup Table

# Description

Construct and return a six-element integer array whose value at each index is the square of that index. The supplied global constant evaluates the builder at compile time. This trains computed lookup-table construction with a constant-evaluable loop.

# Solution

```cpp
std::array<int, 6> result{};
for (std::size_t index = 0; index < result.size(); ++index) {
    result[index] = static_cast<int>(index * index);
}
return result;
```

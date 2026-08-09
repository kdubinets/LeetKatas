# Name

Copy Stream Contents

# Description

Transfer all remaining characters from a caller-provided `std::istream&` into a distinct caller-provided `std::ostream&` through stream-buffer iterators. Both streams remain caller-owned and no intermediate string should be constructed. Return whether every character was accepted by the destination; an empty source is a successful no-op. This exercise covers direct textual stream-buffer transfer and output failure detection.

# Solution

```cpp
auto result = std::ranges::copy(
    std::istreambuf_iterator<char>{source},
    std::istreambuf_iterator<char>{},
    std::ostreambuf_iterator<char>{destination});
return !result.out.failed();
```

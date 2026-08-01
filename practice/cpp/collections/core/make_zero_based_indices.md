# Name

Make Zero-Based Indices

# Description

Create a `std::vector<std::size_t>` of the requested length and fill it with consecutive values from zero through `count - 1`. A zero count must produce an empty vector. This exercise covers generating a consecutive numeric sequence in an existing range.

# Solution

```cpp
std::iota(indices.begin(), indices.end(), std::size_t{0});
```

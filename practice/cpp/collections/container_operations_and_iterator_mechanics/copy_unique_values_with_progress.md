# Name

Copy Unique Values with Progress

# Description

Copy one integer from each run of adjacent equal values in the read-only `input` span into `output`. The output span has capacity for `input.size()` values. Preserve order and return both the number of input elements consumed and the number of output elements written by using both iterator fields of the C++20 ranges algorithm result. This exercise covers consuming a ranges result whose input and output progress can differ.

# Solution

```cpp
auto result = std::ranges::unique_copy(input, output.begin());
return {
    static_cast<std::size_t>(result.in - input.begin()),
    static_cast<std::size_t>(result.out - output.begin())};
```

# Name

Materialize a Range Window

# Description

From a const integer vector, copy at most `count` values after skipping `offset` values. Either number may exceed the input size, and the input must remain unchanged. This exercise covers composing lazy offset and bound views and materializing them in C++20.

# Solution

```cpp
auto window = values | std::views::drop(offset) | std::views::take(count);
std::ranges::copy(window, std::back_inserter(result));
```

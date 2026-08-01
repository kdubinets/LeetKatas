# Name

Square First Values Through Views

# Description

Return `long long` squares of at most the first `count` integers from a const vector, preserving order and naturally using the whole input when `count` is larger than its size. This exercise covers composing bounded and transforming C++20 views before materializing output.

# Solution

```cpp
const auto bounded_count = std::min(count, values.size());
auto squares = values |
               std::views::take(static_cast<std::vector<int>::difference_type>(
                   bounded_count)) |
               std::views::transform([](int value) {
                   return static_cast<long long>(value) * value;
               });
std::ranges::copy(squares, std::back_inserter(result));
```

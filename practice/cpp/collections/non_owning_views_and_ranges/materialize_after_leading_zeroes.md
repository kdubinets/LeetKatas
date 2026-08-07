# Name

Materialize After Leading Zeroes

# Description

Copy a const integer vector after discarding its maximal leading run of zeroes. Zeroes appearing after the first nonzero value must be retained. This exercise covers lazily dropping a predicate-defined prefix.

# Solution

```cpp
auto suffix = values | std::views::drop_while([](int value) {
    return value == 0;
});
std::ranges::copy(suffix, std::back_inserter(result));
```

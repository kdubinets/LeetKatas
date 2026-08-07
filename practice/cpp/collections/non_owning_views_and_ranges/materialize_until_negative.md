# Name

Materialize Until Negative

# Description

Copy the longest leading prefix of a const integer vector containing only nonnegative values. Stop before the first negative value and leave the input unchanged. This exercise covers a lazy predicate-bounded prefix view.

# Solution

```cpp
auto prefix = values | std::views::take_while([](int value) {
    return value >= 0;
});
std::ranges::copy(prefix, std::back_inserter(result));
```

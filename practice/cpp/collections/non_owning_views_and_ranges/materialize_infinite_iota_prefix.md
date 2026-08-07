# Name

Materialize an Infinite Iota Prefix

# Description

Return exactly `count` consecutive representable integers beginning at `first`. Begin with an unbounded lazy integer sequence, limit it safely, and materialize the bounded prefix. This exercise covers adapting an unreachable sentinel with a finite take view.

# Solution

```cpp
auto values = std::views::iota(first) | std::views::take(count);
std::ranges::copy(values, std::back_inserter(result));
```

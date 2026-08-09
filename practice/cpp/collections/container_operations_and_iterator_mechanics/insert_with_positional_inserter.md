# Name

Insert with a Positional Inserter

# Description

Transform every string in the const source vector to its `std::size_t` length and insert those lengths into `destination` immediately before the valid mutable and stable `position`. Preserve source order and all existing list order. This exercise covers adapting generated algorithm output to repeated insertion at a general container position.

# Solution

```cpp
std::ranges::transform(
    source, std::inserter(destination, position),
    [](const std::string& value) { return value.size(); });
```

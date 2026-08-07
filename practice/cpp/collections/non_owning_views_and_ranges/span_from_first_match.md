# Name

Span from First Match

# Description

Search a read-only integer span and return a span beginning at the first target occurrence and ending with the input. Return an empty end-position span when no match exists. This exercise covers using a borrowed algorithm iterator to construct a safe non-owning result.

# Solution

```cpp
auto position = std::ranges::find(values, target);
return {position, static_cast<std::size_t>(values.end() - position)};
```

# Name

Remove a String View Suffix

# Description

Mutate a `std::string_view` boundary so it excludes the final `count` characters, where the count is valid. The underlying characters are neither changed nor copied. This exercise covers narrowing a non-owning string view from its end.

# Solution

```cpp
text.remove_suffix(count);
```

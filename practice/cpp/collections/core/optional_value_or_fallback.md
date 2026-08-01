# Name

Optional Value or Fallback

# Description

Return the integer held by a const `std::optional<int>` when it has a value, or return a supplied fallback integer when it is empty. This exercise covers concise optional consumption without changing the optional.

# Solution

```cpp
return value.value_or(fallback);
```

# Name

Write a Key-Value Record

# Description

Write `key=value` followed by a newline to a caller-provided `std::ostream&`, then return whether the stream remains successful. The key is a non-owning `std::string_view` and the stream remains caller-owned. This exercise covers direct record emission and output-state reporting without constructing an intermediate string.

# Solution

```cpp
output << key << '=' << value << '\n';
return static_cast<bool>(output);
```

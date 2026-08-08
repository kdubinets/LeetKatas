# Name

Hash a Custom Value

# Description

Implement a hash policy for a key whose identity consists of an integer organization and string name. Incorporate both fields using their standard hashes and a conventional combine step.

# Solution

```cpp
const auto first = std::hash<int>{}(key.organization);
const auto second = std::hash<std::string>{}(key.name);
return first ^ (second + 0x9e3779b9U + (first << 6U) + (first >> 2U));
```

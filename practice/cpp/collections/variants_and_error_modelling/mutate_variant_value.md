# Name

Mutate the Active Variant Value

# Description

Mutate the active alternative through one visitor: double an integer, or append a copy of a string to itself. The variant must keep the same active type.

# Solution

```cpp
std::visit([](auto& item) { item += item; }, value);
```

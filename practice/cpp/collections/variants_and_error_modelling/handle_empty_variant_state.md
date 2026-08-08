# Name

Handle an Empty Variant State

# Description

Return whether a selection variant is in its explicit no-selection state. The other alternatives contain an integer or string choice.

# Solution

```cpp
return std::holds_alternative<std::monostate>(selection);
```

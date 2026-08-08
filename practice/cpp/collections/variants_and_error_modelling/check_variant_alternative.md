# Name

Check a Variant Alternative

# Description

Return whether the const variant currently contains its `std::string` alternative without extracting or modifying it. This trains safe variant state inspection.

# Solution

```cpp
return std::holds_alternative<std::string>(value);
```

# Name

Search Map Values Through a View

# Description

Return whether a const ordered map contains a mapped integer equal to the target, without searching or copying its keys. This exercise covers projecting associative entries into a lazy mapped-value view before applying a range algorithm.

# Solution

```cpp
auto mapped_values = values | std::views::values;
return std::ranges::find(mapped_values, target) != mapped_values.end();
```

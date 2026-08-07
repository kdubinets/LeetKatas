# Name

Format a Centered Label

# Description

Center a `std::string_view` within an asterisk-filled field whose nonnegative minimum width is supplied at runtime. A label already at least as wide as the field remains untruncated. This exercise covers fill, center alignment, and a dynamic width argument in `std::format`.

# Solution

```cpp
return std::format("{:*^{}}", label, width);
```

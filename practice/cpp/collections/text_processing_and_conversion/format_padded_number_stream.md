# Name

Format a Padded Number

# Description

Format an `int` as right-aligned decimal text with a caller-selected fill character and minimum field width. The width is nonnegative; values longer than the width are not truncated. This exercise covers one-field stream width and fill configuration.

# Solution

```cpp
std::ostringstream output;
output << std::setfill(fill) << std::setw(width) << value;
return output.str();
```

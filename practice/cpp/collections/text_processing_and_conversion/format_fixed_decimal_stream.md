# Name

Format Fixed Decimal Stream Output

# Description

Return a `double` formatted through a string stream in fixed notation with the requested number of digits after the decimal point. The precision is nonnegative. This exercise covers persistent floating-point output state using standard stream manipulators.

# Solution

```cpp
std::ostringstream output;
output << std::fixed << std::setprecision(precision) << value;
return output.str();
```

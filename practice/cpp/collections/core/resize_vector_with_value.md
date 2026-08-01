# Name

Resize Vector with Value

# Description

Resize a mutable integer vector to a supplied `std::size_t`. Remove trailing elements when shrinking, or initialize every added element to a supplied integer when growing. This exercise covers value-initialized sequence resizing.

# Solution

```cpp
values.resize(new_size, added_value);
```

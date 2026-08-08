# Name

Visit with an Overload Set

# Description

Visit a const integer-or-string variant using separate handlers. Return the integer's nonnegative magnitude as `std::size_t`, or the string length. Inputs do not contain the minimum `int` value.

# Solution

```cpp
return std::visit(Overloaded{
    [](int item) { return static_cast<std::size_t>(item < 0 ? -item : item); },
    [](const std::string& item) { return item.size(); }
}, value);
```

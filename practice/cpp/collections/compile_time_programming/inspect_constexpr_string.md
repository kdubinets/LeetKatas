# Name

Inspect a Constexpr String

# Description

During constant evaluation, create an owning string containing `compile`, append `-time`, and return whether the result equals `compile-time`. The temporary string must release its storage before evaluation completes. This trains C++20 constexpr `std::string` mutation and inspection.

# Solution

```cpp
std::string text = "compile";
text += "-time";
return text == "compile-time";
```

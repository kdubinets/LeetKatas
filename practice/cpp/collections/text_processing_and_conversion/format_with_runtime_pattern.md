# Name

Format with a Runtime Pattern

# Description

Apply a runtime `std::string_view` format pattern to two arguments in order: a text label and an `int`. Return the resulting `std::string`; the caller guarantees that the pattern is valid for those arguments. This exercise covers runtime formatting with a type-erased C++20 format-argument store.

# Solution

```cpp
return std::vformat(pattern, std::make_format_args(label, value));
```

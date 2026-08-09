# Name

Store UTF-8 Code Units

# Description

Return a `std::u8string_view` over the UTF-8 literal `u8"café"`. Preserve C++20's distinct `char8_t` code-unit type rather than converting to `char` text.

# Solution

```cpp
return std::u8string_view{u8"café"};
```

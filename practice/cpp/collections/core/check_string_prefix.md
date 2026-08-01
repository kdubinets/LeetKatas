# Name

Check String Prefix

# Description

Return whether a non-owning `std::string_view` begins with another string view, with an empty prefix matching every input. Neither view's underlying characters may be modified. This exercise covers C++20 prefix testing on string views.

# Solution

```cpp
return text.starts_with(prefix);
```

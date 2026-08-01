# Name

Drop String View Prefix

# Description

Given a non-owning `std::string_view` and a valid `count <= text.size()`, return a view of the same characters after removing the first `count`. No characters are copied or modified. This exercise covers adjusting a non-owning view's starting boundary.

# Solution

```cpp
text.remove_prefix(count);
return text;
```

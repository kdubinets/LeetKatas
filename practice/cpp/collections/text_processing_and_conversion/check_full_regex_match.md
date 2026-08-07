# Name

Check a Complete Regular-Expression Match

# Description

Return whether a precompiled `std::regex` matches an entire const `std::string`. A pattern matching only a substring must produce false. This exercise covers choosing the whole-input regular-expression operation while reusing a compiled pattern.

# Solution

```cpp
return std::regex_match(text, pattern);
```

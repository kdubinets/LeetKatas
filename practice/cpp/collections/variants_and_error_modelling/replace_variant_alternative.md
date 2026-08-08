# Name

Replace a Variant Alternative In Place

# Description

Replace a mutable integer-or-string variant with a string constructed from a count and character, then return a reference to the stored string. This trains direct alternative emplacement.

# Solution

```cpp
return value.emplace<std::string>(count, ch);
```

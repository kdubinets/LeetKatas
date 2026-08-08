# Name

Look Up a Set Key Heterogeneously

# Description

Test membership in a const set of owning `Name` keys using a `std::string_view` target. The supplied transparent comparator permits lookup without constructing or allocating a `Name`.

# Solution

```cpp
return names.contains(target);
```

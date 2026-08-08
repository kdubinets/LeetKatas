# Name

Extract Stem and Extension

# Description

Return a pair containing the lexical stem and extension of the path's final filename component. Both results remain `std::filesystem::path` values so platform path encoding is preserved.

# Solution

```cpp
return {value.stem(), value.extension()};
```

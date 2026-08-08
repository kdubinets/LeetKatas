# Name

Convert Absence to an Explicit Error

# Description

Convert an optional owned string into a string-or-error result. Move present text into the success state and represent absence with `Error::missing`, making the reason for failure explicit.

# Solution

```cpp
if (value) {
    return std::move(*value);
}
return Error::missing;
```

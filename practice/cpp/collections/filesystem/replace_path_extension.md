# Name

Replace a Path Extension

# Description

Replace the final extension of a path value and return the modified path. The caller's original is protected by the by-value parameter; an empty replacement removes an existing extension.

# Solution

```cpp
value.replace_extension(extension);
return value;
```

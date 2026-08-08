# Name

Replace a Path Filename

# Description

Replace a path value's final filename component and return the modified path. Preserve the parent path, and protect the caller's original through the by-value input parameter.

# Solution

```cpp
value.replace_filename(filename);
return value;
```

# Name

Append a Filename Suffix

# Description

Append the native path representation of `suffix` directly to a path value and return the result. Do not insert a directory separator; for example, appending `.bak` to `report.txt` must produce `report.txt.bak` rather than a child path.

# Solution

```cpp
value += suffix;
return value;
```

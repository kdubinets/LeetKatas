# Name

Close a File with a Unique Owner

# Description

Open a C file at `path` in read mode and return a `FileOwner` that automatically calls the matching close operation when non-null. A failed open may produce an empty owner. This exercise covers adapting a standard C resource to RAII with a custom deleter.

# Solution

```cpp
return FileOwner{std::fopen(path, "r")};
```

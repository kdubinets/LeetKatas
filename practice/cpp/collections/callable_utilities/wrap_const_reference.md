# Name

Wrap a Const Reference

# Description

Return a copyable non-owning wrapper around a const string without copying its contents or permitting mutation. The caller guarantees that the string outlives the returned wrapper.

# Solution

```cpp
return std::cref(text);
```

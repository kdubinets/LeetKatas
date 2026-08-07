# Name

Adopt a Legacy Resource

# Description

Call `legacy_create`, whose non-null raw result transfers ownership to the caller, and return that result immediately under `std::unique_ptr<Resource>` ownership. This exercise covers adopting a raw owning result at a legacy API boundary.

# Solution

```cpp
return std::unique_ptr<Resource>{legacy_create(id)};
```

# Name

Specialize a Type Mapping

# Description

Fully specialize `storage_type` for `const char*` so its nested `type` is `std::string`. Other source types must continue to use the primary template.

# Solution

```cpp
template <>
struct storage_type<const char*> {
    using type = std::string;
};
```

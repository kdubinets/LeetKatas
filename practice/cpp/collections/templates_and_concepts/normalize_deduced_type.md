# Name

Normalize a Deduced Type

# Description

Define alias template `normalized_t<T>` that removes any reference and top-level `const` or `volatile` qualification in one C++20 type transformation.

# Solution

```cpp
using normalized_t = std::remove_cvref_t<T>;
```

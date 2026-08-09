# Name

Define an Alias Template

# Description

Define `Sequence<T>` as an alias template for `std::vector<T>`. The alias must form a different vector type for each supplied element type.

# Solution

```cpp
template <class T>
using Sequence = std::vector<T>;
```

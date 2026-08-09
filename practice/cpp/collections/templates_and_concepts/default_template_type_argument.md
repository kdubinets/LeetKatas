# Name

Default a Template Type Argument

# Description

Define alias template `PreferredBox<T>` for `Box<T>`. Give `T` a default template argument of `std::string` while still allowing callers to select another type explicitly.

# Solution

```cpp
template <class T = std::string>
using PreferredBox = Box<T>;
```

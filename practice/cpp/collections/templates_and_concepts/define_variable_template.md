# Name

Define a Variable Template

# Description

Define the compile-time Boolean variable template `is_pointer_type<T>`. Its value must mirror the standard pointer type trait for each supplied type.

# Solution

```cpp
template <class T>
inline constexpr bool is_pointer_type = std::is_pointer_v<T>;
```

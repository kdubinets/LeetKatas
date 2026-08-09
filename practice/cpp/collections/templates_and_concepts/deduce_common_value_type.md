# Name

Deduce a Common Value Type

# Description

Define alias template `common_value_t<Types...>` using the standard type transformation that selects a type to which all supplied types can be implicitly converted. It must accept more than two input types.

# Solution

```cpp
std::common_type_t<Types...>;
```

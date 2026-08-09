# Name

Require a Nested Type

# Description

Define `HasValueType<T>` with a type requirement that checks for the nested name `T::value_type` without constructing a value.

# Solution

```cpp
concept HasValueType = requires {
    typename T::value_type;
};
```

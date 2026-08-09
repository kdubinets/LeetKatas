# Name

Use a Dependent Type Name

# Description

Define `element_type_t<Container>` as the nested `value_type` declared by `Container`. Because the nested name depends on a template parameter, identify it as a type.

# Solution

```cpp
typename Container::value_type;
```

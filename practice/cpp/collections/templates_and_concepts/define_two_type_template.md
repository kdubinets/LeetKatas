# Name

Define a Two-Type Template

# Description

Define `make_values` with two independently deduced by-value parameter types. Return the values in a `std::pair` whose element types preserve those deductions.

# Solution

```cpp
template <class First, class Second>
std::pair<First, Second> make_values(First first, Second second) {
    return {first, second};
}
```

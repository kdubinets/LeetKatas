# Name

Erase Vector Value at Index

# Description

Remove the element at a valid `std::size_t` index from a mutable integer vector, shifting later elements toward the front. The index is guaranteed smaller than the vector size. This exercise covers erasing a sequence element through an iterator position.

# Solution

```cpp
values.erase(
    values.begin() + static_cast<std::vector<int>::difference_type>(index));
```

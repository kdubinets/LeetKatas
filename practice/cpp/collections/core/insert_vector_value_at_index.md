# Name

Insert Vector Value at Index

# Description

Insert an integer into a mutable vector immediately before a valid `std::size_t` index satisfying `index <= values.size()`. An index equal to the size appends the value. This exercise covers converting a validated index into a sequence insertion position.

# Solution

```cpp
values.insert(
    values.begin() + static_cast<std::vector<int>::difference_type>(index),
    value);
```

# Name

Materialize Reverse Iterators

# Description

Construct and return a `std::vector<int>` containing a const list's elements from last to first, using the vector's legacy iterator-pair construction interface. Leave the list unchanged. This exercise covers direct use of a container's reverse iterators when an iterator-pair API is required.

# Solution

```cpp
return std::vector<int>(values.rbegin(), values.rend());
```

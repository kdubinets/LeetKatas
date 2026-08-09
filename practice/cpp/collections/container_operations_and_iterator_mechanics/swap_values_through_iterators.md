# Name

Swap Values Through Iterators

# Description

Exchange the values referenced by two iterators satisfying `std::indirectly_swappable`, allowing iterator-specific swap customization to participate. This exercise covers the C++20 ranges iterator-swap customization point in a constrained generic operation.

# Solution

```cpp
std::ranges::iter_swap(left, right);
```

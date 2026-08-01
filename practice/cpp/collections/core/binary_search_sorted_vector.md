# Name

Binary Search a Sorted Vector

# Description

Return whether an integer target occurs in a const ascending `std::vector<int>` without modifying the vector. This exercise covers direct logarithmic membership testing in a sorted range.

# Solution

```cpp
return std::ranges::binary_search(sorted_values, target);
```

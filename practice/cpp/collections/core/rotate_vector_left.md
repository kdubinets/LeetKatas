# Name

Rotate Vector Left Once

# Description

Mutate a `std::vector<int>` by moving its first element to the end while preserving the order of the other elements; an empty vector must remain unchanged. This exercise covers rotation with a safely chosen middle iterator.

# Solution

```cpp
if (!values.empty()) {
    std::ranges::rotate(values, values.begin() + 1);
}
```

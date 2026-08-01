# Name

Find All Target Indices

# Description

Return all `std::size_t` indices at which a target integer occurs in a const vector, ordered from smallest to largest, without modifying the input. This exercise covers safe index-based iteration and collection of matching positions.

# Solution

```cpp
for (std::size_t index = 0; index < values.size(); ++index) {
    if (values[index] == target) {
        indices.push_back(index);
    }
}
```

# Name

Build Adjacent Differences

# Description

Return a `std::vector<long long>` whose first element equals the first input value and whose later elements equal the current integer minus its predecessor. An empty input produces an empty output, and subtraction must use `long long`. This exercise covers adjacent numeric transformation.

# Solution

```cpp
std::adjacent_difference(
    values.begin(), values.end(), result.begin(),
    [](int current, int previous) {
        return static_cast<long long>(current) - previous;
    });
```

# Name

Apply Closed Range Additions

# Description

Use a difference array to apply every inclusive `RangeAddition` to an initially zero-filled result of `size` values. Each update is in bounds and has `first <= last`. Record the change at both boundaries, then materialize the final values with one running total rather than updating every covered element per operation.

# Solution

```cpp
std::vector<long long> differences(size + 1, 0);
for (const RangeAddition& update : updates) {
    differences[update.first] += update.delta;
    differences[update.last + 1] -= update.delta;
}

std::vector<long long> result(size);
long long current = 0;
for (std::size_t index = 0; index < size; ++index) {
    current += differences[index];
    result[index] = current;
}
return result;
```

# Name

Partition Negative Values First

# Description

Use opposing partition pointers to rearrange `values` so all negative values precede all nonnegative values, then return the index of the first nonnegative value. Mutation need not preserve order. Maintain the two completed regions at the sequence ends while the unresolved region shrinks.

# Solution

```cpp
std::size_t left = 0;
std::size_t right = values.size();
while (left < right) {
    if (values[left] < 0) {
        ++left;
        continue;
    }
    --right;
    std::swap(values[left], values[right]);
}
return left;
```

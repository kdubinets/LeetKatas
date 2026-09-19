# Name

Partition Negative Values First

# Description

Rearrange `values` in place so all negative values precede all values greater than or equal to zero. Return the first nonnegative index, or `values.size()` if no such element exists. Either group's order may change. Empty input returns zero.

The supplied pattern is opposing partition pointers whose completed left region is negative and completed right region is nonnegative.

This exercise covers maintaining completed regions at opposing sequence boundaries during unstable in-place partitioning.

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

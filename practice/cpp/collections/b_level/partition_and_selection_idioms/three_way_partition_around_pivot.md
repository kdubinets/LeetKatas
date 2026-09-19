# Name

Three-Way Partition around a Pivot

# Description

Rearrange values into below-pivot, equal-pivot, and above-pivot regions, preserving multiplicity and size but not internal order. Return the half-open equal-region boundaries; when no value equals pivot, that region is empty.

The supplied four-region invariant classifies one unknown value at a time while maintaining less, equal, unknown, and greater regions.

This exercise covers four-region transitions in a Dutch-national-flag partition.

# Solution

```cpp
std::size_t less = 0;
std::size_t scan = 0;
std::size_t greater = values.size();
while (scan < greater) {
    if (values[scan] < pivot) {
        std::swap(values[less++], values[scan++]);
    } else if (values[scan] > pivot) {
        std::swap(values[scan], values[--greater]);
    } else {
        ++scan;
    }
}
return {less, greater};
```

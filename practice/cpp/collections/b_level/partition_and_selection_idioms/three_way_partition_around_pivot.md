# Name

Three-Way Partition around a Pivot

# Description

Rearrange values into below-pivot, equal-pivot, and above-pivot regions, preserving multiplicity and size while allowing arbitrary internal order. Return zero-based half-open equal-region boundaries. If no value equals pivot, the boundaries are equal at the position after all smaller values; empty input returns {0, 0}. The pivot need not occur in the input.

Use the supplied four-region invariant to classify one unknown value at a time while maintaining less, equal, unknown, and greater regions.

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

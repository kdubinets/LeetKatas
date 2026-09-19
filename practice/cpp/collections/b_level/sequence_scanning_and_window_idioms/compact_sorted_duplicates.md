# Name

Compact Sorted Duplicate Runs

# Description

Modify the prefix of `values` to contain each distinct input value exactly once, in sorted order, and return that prefix's length. Keep the vector's size unchanged; elements beyond the returned length are unspecified. The input is sorted in nondecreasing order. Empty input has a retained prefix of length zero.

The supplied pattern is read/write pointers: the written prefix contains each distinct value encountered so far exactly once, in input order.

This exercise covers maintaining a deduplicated prefix with read/write pointers over sorted runs.

# Solution

```cpp
if (values.empty()) {
    return 0;
}

std::size_t write = 1;
for (std::size_t read = 1; read < values.size(); ++read) {
    if (values[read] != values[write - 1]) {
        values[write] = values[read];
        ++write;
    }
}
return write;
```

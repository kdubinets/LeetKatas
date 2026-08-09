# Name

Compact Sorted Duplicate Runs

# Description

Use read/write pointers to compact ascending `values` in place so its prefix contains exactly one value from each equal run. Return the new prefix length; values after that length are irrelevant. The completed prefix is the invariant that makes each read value easy to compare.

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

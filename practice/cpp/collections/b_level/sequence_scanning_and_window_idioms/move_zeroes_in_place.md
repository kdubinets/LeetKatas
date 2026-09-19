# Name

Move Zeroes to the End In Place

# Description

Rearrange `values` in place so all nonzero values retain their original order and are followed by all zeroes. Keep the vector's size unchanged. Empty input stays empty.

The supplied pattern is read/write pointers whose written prefix contains the nonzero values encountered so far in their original order.

This exercise covers stable in-place compaction of selected values with read/write pointers.

# Solution

```cpp
std::size_t write = 0;
for (std::size_t read = 0; read < values.size(); ++read) {
    if (values[read] != 0) {
        std::swap(values[write], values[read]);
        ++write;
    }
}
```

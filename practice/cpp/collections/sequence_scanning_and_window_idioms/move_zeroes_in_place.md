# Name

Move Zeroes to the End In Place

# Description

Use read/write pointers to move every zero in `values` to its end while preserving the relative order of its nonzero values. Mutate `values` in place. The completed prefix must always contain the nonzero values encountered so far in order.

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

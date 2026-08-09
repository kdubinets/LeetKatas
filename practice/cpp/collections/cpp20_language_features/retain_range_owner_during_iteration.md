# Name

Retain a Range Owner During Iteration

# Description

Use a C++20 range-for init-statement to bind the result of `load_numbers()` to a local owner, then iterate over the range returned by its `view()` member and add each integer to `total`. The owner must span the loop so the returned reference remains valid.

# Solution

```cpp
for (auto numbers = load_numbers(); int value : numbers.view()) {
    total += value;
}
```

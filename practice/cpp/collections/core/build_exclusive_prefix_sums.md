# Name

Build Exclusive Prefix Sums

# Description

Return a `std::vector<long long>` where each position contains the sum of input values strictly before that position, making the first output zero. The output is already sized, and accumulation must use `long long`. This exercise covers an exclusive numeric scan.

# Solution

```cpp
std::exclusive_scan(values.begin(), values.end(), result.begin(), 0LL);
```

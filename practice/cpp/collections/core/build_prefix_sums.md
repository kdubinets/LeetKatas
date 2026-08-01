# Name

Build Prefix Sums

# Description

Return a `std::vector<long long>` where each element is the sum of the const integer input from its beginning through the corresponding position. The output is already sized, and summation must use `long long`. This exercise covers an inclusive numeric scan into a separate range.

# Solution

```cpp
std::inclusive_scan(values.begin(), values.end(), result.begin(),
                    std::plus<>{}, 0LL);
```

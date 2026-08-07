# Name

Compare Signed and Unsigned Values

# Description

Return whether an `int` is mathematically less than an `unsigned int`. Negative signed values must compare less, without accidental conversion to a large unsigned value. This exercise covers C++20 safe mixed-signedness integer comparison.

# Solution

```cpp
return std::cmp_less(left, right);
```

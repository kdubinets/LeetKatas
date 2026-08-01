# Name

Greatest Common Divisor of Values

# Description

Return the greatest common divisor of all values in a const vector of nonnegative integers, returning zero for an empty vector. The input must remain unchanged. This exercise covers folding a range with a standard numeric utility.

# Solution

```cpp
return std::accumulate(values.begin(), values.end(), 0,
                       [](int result, int value) {
                           return std::gcd(result, value);
                       });
```

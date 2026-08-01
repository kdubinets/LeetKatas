# Name

Unzip Pairs

# Description

Convert a const vector of `(int, string)` pairs into a pair of vectors: all integer fields in the first and all string fields in the second, preserving input order. Both output capacities are already reserved. This exercise covers structured binding over pairs and constructing parallel outputs.

# Solution

```cpp
for (const auto& [number, text] : values) {
    result.first.push_back(number);
    result.second.push_back(text);
}
```

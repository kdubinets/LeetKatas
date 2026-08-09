# Name

Transform an Array at Compile Time

# Description

Fill the supplied result array with the squares of the input elements and return it, with transformation usable during constant evaluation. This covers the C++20 constant-evaluable standard transform algorithm.

# Solution

```cpp
std::transform(values.begin(), values.end(), result.begin(),
               [](int value) { return value * value; });
return result;
```

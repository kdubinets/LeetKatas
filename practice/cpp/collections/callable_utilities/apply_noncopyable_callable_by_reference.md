# Name

Apply a Non-Copyable Callable by Reference

# Description

Apply the existing non-copyable `Sum` object to every integer in a const vector so its `total` accumulates all values. Adapt the object for the ranges algorithm's by-value callable parameter without copying the state.

# Solution

```cpp
std::ranges::for_each(values, std::ref(sum));
```

# Name

Capture an Argument Pack by Value

# Description

Return a zero-argument lambda that uses a C++20 pack init-capture to own each forwarded argument. When invoked, expand the captured values into a tuple.

# Solution

```cpp
return [...values = std::forward<Args>(args)] {
    return std::tuple{values...};
};
```

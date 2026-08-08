# Name

Combine Two Optional Values

# Description

Construct an optional pair only when both input optionals contain integers; otherwise return absence. This trains propagation of multiple required optional inputs.

# Solution

```cpp
if (x && y) {
    return std::pair{*x, *y};
}
return std::nullopt;
```

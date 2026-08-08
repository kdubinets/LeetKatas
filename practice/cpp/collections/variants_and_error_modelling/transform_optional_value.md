# Name

Transform an Optional Value

# Description

Map an optional string to its length while preserving absence. This exercises the explicit C++20 form of value-preserving optional composition.

# Solution

```cpp
if (text) {
    return text->size();
}
return std::nullopt;
```
